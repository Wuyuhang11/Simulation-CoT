from tqdm import tqdm  # 进度条库，用于可视化任务进度
import re  # 正则表达式库，用于字符串模式匹配
import ast  # 抽象语法树库，用于解析Python字符串格式的代码
import sympy  # 一个用于符号计算的Python库
import time  # 用于处理基于时间的操作，例如延迟
import json
from excute.prompt.math_prompt import abstract_prompt, relation_prompt, generate_example_prompt, \
    sliding_window_example_prompt, report_prompt, simulation_response_prompt  # math_prompt
from model.api.llama_model_api import get_simulation_cot_abstraction, get_simulation_cot_relation, \
    get_simulation_cot_example, get_simulation_cot_window, get_simulation_cot_report, \
    get_simulation_cot_response  # simulation_cot

"""
1.超参数设置
"""
model_name = "llama3-8B"
dataset = "../../data/MATH/test.jsonl"
problem_level_lower_bound = 1  # 题目最低难度
problem_level_upper_bound = 5  # 题目最高难度
problem_interval_begin = 0  # 题目区间开始
problem_interval_end = 500  # 题目区间结束
t = time.localtime()
TRY_CNT = 8
valid_correctness = ["正确", "错误"] # 定义选项集

logfilename = '../results/results-math-simulation-cot--' + model_name + '--' + 'math' + '--k_' + '--' + time.strftime(
    "%Y-%m-%d-%H-%M-%S", t) + '.jsonl'

"""
2.从JSONL文件中加载数据
"""
data = []
with open(dataset, 'r', encoding='utf-8') as f:
    cnt = 0  # 初始化计数器
    for line in f:
        # 根据题目难度筛选数据
        if (json.loads(line)['level'] < problem_level_lower_bound):
            continue  # 跳过不符合条件的数据
        if (json.loads(line)['level'] > problem_level_upper_bound):
            continue
        data.append(json.loads(line))  # 符合条件的题目加载到列表中
        cnt += 1

# 截取指定区间的数据
data = data[problem_interval_begin:problem_interval_end + 1]
print(f"数据集大小:{len(data)}")

"""
3.日志文件配置,
"""
with open(logfilename, 'w') as f:
    f.write("模型: " + model_name + "\n")
    f.write("数据集: MATH - " + dataset + "\n")
    f.write(f"问题难度区间：[{problem_level_lower_bound},{problem_level_upper_bound}]\n")
    f.write(f"数据集大小：[{len(data)}]\n")
    f.write("--------------------------------\n")

"""
4.从数据集data中加载每个题目，实现Simulation——CoT对每个问题进行解答
"""
correct_answers = 0  # 正确答案数
cnt = 0  # 计数器
total_cnt = len(data)  # 题目总数

for example in tqdm(data, desc="评估中", unit="例"):  # 遍历从数据集中加载的每个题目，并用tqdm显示评估进度
    cnt += 1

    # 加载每一个题目
    print("-------------------------\n### 示例ID: ", example["unique_id"], "\t ( ", cnt, "/", total_cnt, " )")
    print("[问题难度]: ", example["level"])
    print("[问题主题]: ", example["subject"])
    print("[问题内容]: ", example["problem"])

    try_cnt = 0  # 尝试次数
    while True:
        try_cnt += 1
        try:
            # 1.得到背景知识
            background_concepts = get_simulation_cot_abstraction(example["problem"], abstract_prompt)  # 得到问题后的背景知识
            bg_list = re.findall(r"\d+\.s+([^:]+):", background_concepts)  # 背景知识集合
            print("[背景知识]: ", bg_list)

            # 2.根据背景知识生成彼此相关的字典序relation_map
            relation_map = {}
            for i in range(len(bg_list) - 1):
                concept1 = bg_list[i]
                concept2 = bg_list[i + 1]
                relation_input = relation_prompt.replace("{{concept1}}", concept1).replace("{{concept2}}", concept2)
                relation_desc = get_simulation_cot_relation(relation_input)  # 得到概念之间的关系
                relation_map[relation_desc] = 0  # k-v；(r,0/1)；默认为0
                print("[背景知识]: ", relation_map)

            # 3.根据每一个概念生成对应示例
            example_list = []
            for i in range(len(bg_list)):
                example_input = generate_example_prompt.replace("{{concept}}", bg_list[i])  # 置换后的生成示例的prompt
                example_desc = get_simulation_cot_example(example_input)  # 得到示例
                example_list.append(example_desc)  # 添加到集合中
                print("[子例集合]: ", example_list)

            # 4.从第一个示例作为起点，利用滑动窗口的方式对示例进行 【加噪：滑动窗口】 得到新的示例1_2
            relation_iter = iter(relation_map.keys())  # 利用 iter函数 创建一个关于 relation_map 的迭代器
            example_pre = example_list[0]  # 起始示例
            for i in range(len(example_list) - 1):
                example_next = example_list[i + 1]  # 下一步示例
                relation = next(relation_iter, None)  # 获取下一个关系
                if relation is not None:
                    relation_map[relation] = 1  # 将对应关系值置为1
                window_example_input = sliding_window_example_prompt.replace("{{example_pre}}", example_pre
                                                                             ).replace("{{example_next}}", example_next
                                                                                       ).replace("{{relation}}",
                                                                                                 relation)
                new_example = get_simulation_cot_window(window_example_input)  # 得到新示例
                example_pre = new_example  # 滑动窗口

            final_example = example_pre  # 最终的示例
            print("[滑动子例后得到的最终示例]: ", final_example)

            # 5.联系最终示例和背景知识之间的关系，作为一份报告,辅助模型对 final_example 进行【减噪】以【生成最完美的示例】
            report_input = report_prompt.replace("{{example}}", background_concepts).replace("{{background_knowledge}}",
                                                                                             final_example)
            report_final_example = get_simulation_cot_report(report_input)

            # 6.结合报告 report_final_example 和最终示例 final_example 符合lm生成最终响应
            response_input = simulation_response_prompt.replace("{{example}}", final_example).replace("{{report}}",
                                                                                                      report_final_example)
            response_out = get_simulation_cot_response(response_input) # 得到最终答案
