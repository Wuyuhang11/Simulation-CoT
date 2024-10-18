abstract_prompt = """
角色（Role）：  
   你是一名世界级的数学分析家和逻辑学家，能够深入理解问题并提炼出关键概念。

问题分析（Question Analysis）：  
   将接收到的数学问题 Q 进行分析得到背后的概念知识。

要求（Requirements）：  
   1. 从问题 Q 中抽象出关键的概念知识。  
   2. 这些概念知识是解决问题的必要部分。  
   3. 组合这些概念知识可以全面解决问题 Q。  
   4. 提供详细的概念知识描述，避免过于简短。  
   5. 回答中仅包含概念知识，无需其他信息。  

响应格式（Response Format）：  
 - 1. xxxx
 - 2. xxxx
 - 3. xxxx
 - ...  

示例问题（Example Question）：  
   "求一个点在圆上的位置，圆心在原点，已知点的直角坐标系和极坐标系表示。"

示例回复（Example Response）：  
 - 1. 直角坐标到极坐标转换  
 - 2. 半径 \(r\) 的计算  
 - 3. 角度 \(\theta\) 的确定  

Q：{{question}} 
"""

relation_prompt = """
角色：你是一个数学大师，请你根据传入的概念1{concept1}和概念2{concept2}之间的联系，生成二者之间的关系，无需阐述过多内容，只需生成其关系relation即可。
概念1：{{concept1}}
概念2：{{concept2}}
关系：
"""

generate_example_prompt = """
请根据定义的角色、对你的要求、以及生成示例，生成符合要求的响应内容

角色：你是一个数学大师，请你利用自己所知的数学，根据传入的概念--{{concept}}生成相关的示例。

要求：生成的示例包括问题、推理过程、最终答案，并贴合传入的概念--{{concept}}。

生成示例：
  题目：给定表达式 \(2 \cdot 3 \cdot 4\)，根据乘法结合律，计算其可能的不同值。
  推理过程：
    1.按照乘法结合律，无论怎样分组乘法操作，结果应该是相同的。
    2.计算如下：1. \( (2 \cdot 3) \cdot 4 = 6 \cdot 4 = 24 \) 2. \( 2 \cdot (3 \cdot 4) = 2 \cdot 12 = 24 \)
  最终答案：表达式 \(2 \cdot 3 \cdot 4\) 不论如何使用括号，其结果都是 24。这表明，根据乘法的结合律，该表达式的值是唯一的。  
  
"""

sliding_window_example_prompt = """
你是一个数学大师，对于数学问题的运用如火纯青，请你利用 示例1 和 示例2 的内容根据二者之间的 关系r 生成一个包含示例1和示例2的全新示例1_2 ！！

注意：生成的内容只需要包含全新示例1_2，无需生成其他内容！！

示例1：{{example1}}
示例2：{{example2}}
关系r：{{relation}}
"""

generate_report_prompt = """
你是一个数学大师，对于数学的理解如火纯青，请你结合传入的 示例 和传入的 背景集合 生成一个相关报告，这个报告内容包含二者的匹配程度和你对二者的相关分析 ！！

注意：生成的内容只需要包括报告内容，与报告无关的内容请无需生成！！
注意：生成的内容言简意赅，maxtoken=200！！

示例：{{example1}}
背景集合：{{background_concepts}}
"""

answer_prompt = """
你是一个数学大师，请根据传入的 示例 和 报告 回答传入的数学 问题 ，请你逐步思考后回答。

注意：输出的回答内容一定要包含“最终答案：xxx”这个范式！！
注意：请逐步思考，并结合示例和报告回答问题（maxtoken=300）！！

示例：{{example}}
报告：{{report}}
问题：{{question}}
"""
