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
角色：假设你是数学大师，请你根据概念1(concept1)和概念2(concept2)之间的联系，生成二者之间的关系，无需阐述过多内容，只需生成其关系relation即可。
概念1：{{concept1}}
概念2：{{concept2}}
关系：
"""
