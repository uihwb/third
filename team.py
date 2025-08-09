import os
import json
from typing import Dict, Any, List
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

class SolverAgent:
    """多领域求解器"""
    def solve(self, subproblem: Dict) -> Dict:
        try:
            prompt = """你是一个顶尖问题求解专家，请按以下格式解答：

**题目**：（直接重复原始问题）

**分析**：
1. 问题类型识别
2. 关键条件/参数提取
3. 解题方法选择

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
                model="gpt-4-turbo-preview",  # 使用最新GPT-4模型
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"请解答以下问题：\n{subproblem['description']}\n参数：{subproblem.get('params','无')}"}
                ],
                temperature=0.3  # 适当提高创造性以处理复杂问题
            )
            return {"solution": response.choices[0].message.content}
        except Exception as e:
            return {"error": f"求解错误: {str(e)}"}

class AgentTeam:
    def __init__(self):
        self.parser = ParserAgent()
        self.solver = SolverAgent()

    def solve_problem(self, text: str) -> Dict:
        # 解析阶段
        parsed = self.parser.parse(text)
        if "error" in parsed:
            return {"status": "error", "message": parsed["error"]}

        # 求解阶段
        solutions = []
        for sub in parsed.get("subproblems", []):
            solution = self.solver.solve(sub)
            solutions.append({
                "description": sub["description"],
                "result": solution
            })

        return {
            "problem": text,
            "solutions": solutions
        }

if __name__ == "__main__":
    print("高级问题求解系统（输入q退出）")
    team = AgentTeam()
    
    while True:
        try:
            user_input = input("\n请输入问题: ").strip()
            if user_input.lower() == 'q':
                break
            
            result = team.solve_problem(user_input)
            
            if "status" in result and result["status"] == "error":
                print(f"\n❌ 错误: {result['message']}")
            else:
                print("\n" + "="*60)
                print(f"\n**原始问题**: {result['problem']}")
                
                for idx, sol in enumerate(result["solutions"], 1):
                    res = sol['result']
                    
                    if "error" in res:
                        print(f"\n❌ 子问题{idx}错误: {res['error']}")
                        continue
                    
                    print(f"\n{sol['result']['solution']}")
                    print("\n" + "="*60)
                
        except KeyboardInterrupt:
            print("\n程序已退出")
            break
        except Exception as e:
            print(f"\n⚠️ 系统错误: {str(e)}")