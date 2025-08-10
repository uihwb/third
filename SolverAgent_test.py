import os
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

# 环境配置
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SolverAgent:
    """多领域求解器"""
    def solve(self, problem_description: str) -> Dict:
        try:
            prompt = """你是一个顶尖问题求解专家，请按以下格式解答：

**解答过程**：
- 步骤1：（详细说明）
- 步骤2：（详细说明）
- ...（必要时提供验证过程）

**答案**：（明确简洁的最终答案）

要求：
1. 必须严格按此格式输出
2. 确保逻辑严谨无矛盾
3. 数学问题需展示推导过程
4. 逻辑问题需验证所有可能性"""

            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"请解答以下问题：\n{problem_description}"}
                ],
                temperature=0.3
            )
            return {"solution": response.choices[0].message.content}
        except Exception as e:
            return {"error": f"求解错误: {str(e)}"}

if __name__ == "__main__":
    print("问题求解测试系统（输入q退出）")
    solver = SolverAgent()
    
    while True:
        try:
            user_input = input("\n请输入问题: ").strip()
            if user_input.lower() == 'q':
                break
            
            result = solver.solve(user_input)
            
            if "error" in result:
                print(f"\n❌ 错误: {result['error']}")
            else:
                print("\n" + "="*60)
                print(f"\n{result['solution']}")
                print("\n" + "="*60)
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            break
        except Exception as e:
            print(f"\n⚠️ 系统错误: {str(e)}")