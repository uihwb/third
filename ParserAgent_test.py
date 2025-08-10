import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

# 环境配置
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ParserAgent:
    """自然语言解析器"""
    def __init__(self):
        self.system_prompt = """你是一个智能问题解析专家，请：
1. 精确识别问题类型（数学/逻辑/图论/算法等）
2. 提取所有关键参数和条件
3. 输出严格JSON格式：
{
  "type": "问题类型",
  "subproblems": [{
    "description": "问题描述（保留原始问题中的所有关键信息）",
    "params": {参数键值对}
  }]
}"""

    def parse(self, text: str) -> Dict[str, Any]:
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",  # 使用最新GPT-4模型
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"请精确解析以下问题：\n{text}\n输出JSON"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"解析错误: {str(e)}"}

if __name__ == "__main__":
    print("问题解析测试系统（输入q退出）")
    parser = ParserAgent()
    
    while True:
        try:
            user_input = input("\n请输入问题: ").strip()
            if user_input.lower() == 'q':
                break
            
            result = parser.parse(user_input)
            print("\n解析结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        except KeyboardInterrupt:
            print("\n程序已退出")
            break
        except Exception as e:
            print(f"\n⚠️ 系统错误: {str(e)}")