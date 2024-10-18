from tqdm import tqdm  # 进度条库，用于可视化任务进度
import re  # 正则表达式库，用于字符串模式匹配
import time  # 用于处理基于时间的操作，例如延迟
import json
from excute.prompt.math_prompt import abstract_prompt, relation_prompt, generate_example_prompt, \
    sliding_window_example_prompt, generate_report_prompt, answer_prompt, judge_prompt  # math_prompt
from model.api.llama_model_api import get_simulation_cot_abstraction, get_simulation_cot_relation, \
    get_simulation_cot_example, get_simulation_cot_window, get_simulation_cot_report, \
    get_simulation_cot_answer, get_simulation_cot_judgement  # simulation_cot

def main():
    """
    1. 超参数设置
    """
    model_name = "llama3-8B"
    dataset = "../../data/MATH/test.jsonl"
    problem_level_lower_bound = 1  # 题目最低难度
    problem_level_upper_bound = 5  # 题目最高难度
    problem_interval_begin = 0  # 题目区间开始
    problem_interval_end = 500  # 题目区间结束
    t = time.localtime()
    logfilename = '../results/results-math-simulation-cot--' + model_name + '--' + 'math' + '--k_' + '--' + time.strftime(
        "%Y-%m-%d-%H-%M-%S", t) + '.jsonl'

    """
    2. 从JSONL文件中加载数据
    """
    data = []
    with open(dataset, 'r', encoding='utf-8') as f:
        for line in f:
            # 根据题目难度筛选数据
            level = json.loads(line)['level']
            if level < problem_level_lower_bound or level > problem_level_upper_bound:
                continue
            data.append(json.loads(line))  # 符合条件的题目加载到列表中

    # 截取指定区间的数据
    data = data[problem_interval_begin:problem_interval_end + 1]
    print(f"数据集大小: {len(data)}")

    """
    3. 日志文件配置
    """
    with open(logfilename, 'w') as f:
        f.write("模型: " + model_name + "\n")
        f.write("数据集: MATH - " + dataset + "\n")
        f.write(f"问题难度区间：[{problem_level_lower_bound},{problem_level_upper_bound}]\n")
        f.write(f"数据集大小：[{len(data)}]\n")
        f.write("--------------------------------\n")

    """
    4. 从数据集data中加载每个题目
    """
    correct_answers = 0  # 正确答案数
    total_cnt = len(data)  # 题目总数

    for cnt, example in enumerate(tqdm(data, desc="评估中", unit="例"), start=1):
        # 加载每一个题目
        print("-------------------------\n### 示例ID: ", example["unique_id"], "\t ( ", cnt, "/", total_cnt, " )")
        print("[问题难度]: ", example["level"])
        print("[问题主题]: ", example["subject"])
        print("[问题内容]: ", example["problem"])

        try_cnt = 0  # 尝试次数
        while True:
            try_cnt += 1
            try:
                # 1. 得到背景知识
                background_concepts = get_simulation_cot_abstraction(example["problem"], abstract_prompt)
                bg_list = re.findall(r"\d+\.s+([^:]+):", background_concepts)
                print("[背景知识]: ", bg_list)

                # 2. 生成关系字典
                relation_map = {}
                for i in range(len(bg_list) - 1):
                    concept1 = bg_list[i]
                    concept2 = bg_list[i + 1]
                    relation_input = relation_prompt.replace("{{concept1}}", concept1).replace("{{concept2}}", concept2)
                    relation_desc = get_simulation_cot_relation(relation_input)
                    relation_map[relation_desc] = 0
                print("[关系图]: ", relation_map)

                # 3. 生成示例
                example_list = []
                for concept in bg_list:
                    example_input = generate_example_prompt.replace("{{concept}}", concept)
                    example_desc = get_simulation_cot_example(example_input)
                    example_list.append(example_desc)
                print("[示例集合]: ", example_list)

                # 4. 滑动窗口生成新示例
                relation_iter = iter(relation_map.keys())
                example_pre = example_list[0]
                for i in range(len(example_list) - 1):
                    example_next = example_list[i + 1]
                    relation = next(relation_iter, None)
                    if relation is None:
                        break
                    relation_map[relation] = 1
                    window_example_input = sliding_window_example_prompt.replace("{{example_pre}}", example_pre).replace(
                        "{{example_next}}", example_next).replace("{{relation}}", relation)
                    new_example = get_simulation_cot_window(window_example_input)
                    example_pre = new_example

                final_example = example_pre
                print("[最终示例]: ", final_example)

                # 5. 生成报告
                report_input = generate_report_prompt.replace("{{final_example}}", final_example).replace(
                    "{{background_concepts}}", background_concepts)
                report = get_simulation_cot_report(report_input)
                print("[生成的报告]: ", report)

                # 6. 得到最终答案
                answer_input = answer_prompt.replace("{{report}}", report) \
                    .replace("{{example}}", final_example) \
                    .replace("{{question}}", example["problem"])
                answer = get_simulation_cot_answer(answer_input)
                solution = re.search(r"最终答案：([^。]+)", answer).group(1)
                print("[最终答案]: ", answer)
                print("[最终解集]: ", solution)

                # 7. 验证答案
                judge_input = judge_prompt.replace("{{question}}", example["problem"]) \
                    .replace("{{answer}}", answer) \
                    .replace("{{truth_answer}}", example["answer"])

                judge = get_simulation_cot_judgement(judge_input)
                match_judge_content = re.search(r"判断：(\S\S)", judge)

                final_judge = ""
                if match_judge_content:
                    final_judge = match_judge_content.group(1)
                    if final_judge == "正确":
                        correct_answers += 1
                    elif final_judge in ["错误", "未知"]:
                        final_judge = "不正确"
                        match_advisor = re.search(r"建议：(.+)", judge)
                        if match_advisor:
                            advisor = match_advisor.group(1)
                            print("[建议]: ", advisor)
                else:
                    if re.search(r"(?<!不)正确", judge):
                        correct_answers += 1
                        final_judge = "正确"
                    else:
                        final_judge = "不正确"
                        match_advisor = re.search(r"建议：(.+)", judge)
                        if match_advisor:
                            advisor = match_advisor.group(1)
                            print("[建议]: ", advisor)

                print("[最终判断]: ", final_judge)
                print("[当前正确数]: ", correct_answers)

                # 8. 统计准确率
                accuracy = correct_answers / cnt
                print("[当前平均准确率]: ", accuracy)

                # 9. 记录结果
                result = {
                    "当前准确率": accuracy,
                    "示例ID": example["unique_id"],
                    "难度": example["level"],
                    "问题主题": example["subject"],
                    "问题内容": example["problem"],
                    "正确性": final_judge,
                    "最终答案": answer,
                    "最终解": solution,
                    "标准答案": example["answer"],
                    "标准解": example["solution"],
                }

                with open(logfilename, 'a') as f:
                    f.write(json.dumps(result) + '\n')

            except Exception as e:
                print(e)
                time.sleep(min(1024, 2 ** (try_cnt / 2)))
                continue

if __name__ == "__main__":
    main()
