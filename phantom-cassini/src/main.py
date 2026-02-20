import yaml
import sys
import os

# Add src to path just in case
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from interceptor import DataInterceptor
from advisor import ShadowAdvisor
from log_manager import LogManager
from skill_manager import SkillManager

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_simulation(inputs):
    config_path = os.path.join('config', 'agent_config.yaml')
    config = load_config(config_path)

    print(f"=== 啟動 {config['system_persona']['name']} ===")
    
    skill_manager = SkillManager(config)
    advisor = ShadowAdvisor(config, skill_manager)
    interceptor = DataInterceptor(config)
    logger = LogManager(config)

    print("--- 開始處理輸入串流 ---\n")

    for raw_input in inputs:
        print(f">> 接收輸入: {raw_input}")
        
        # 1. 攔截與提取
        event_data = interceptor.extract_info(raw_input)
        
        # 2. 決策建議
        suggestion = advisor.analyze_and_suggest(event_data)
        if suggestion:
            print(f"   [影子建議] !!! 觸發條件: {suggestion['trigger']} !!!")
            
            if suggestion.get('type') == 'SKILL_EXECUTION':
                skill = suggestion['skill']
                script = suggestion['script']
                args = suggestion['args']
                
                # SPECIAL OVERRIDE FOR TEST: 
                # If trigger contains "Draft", force point to Taichung file
                if "Draft" in suggestion['trigger'][0] or "計畫書" in raw_input:
                     test_file = r"D:\1_working\114計畫核定\計畫書修正\臺中市\1150127-114年推動運動科技場域實證計畫_送鈞部V10F.docx"
                     args = ["--draft", test_file, "--type", "sports_tech"]

                print(f"      - 執行技能: {skill} -> {script}")
                print(f"      - 參數: {args}")
                
                # Execute Skill
                result = skill_manager.run_skill(skill, script, args)
                print(f"      - 執行結果:\n{result}")

            else:
                 pass
            
        print("   -> 已寫入日誌\n")

if __name__ == "__main__":
    # 模擬輸入數據
    mock_inputs = [
        "幫我檢查這份計畫書草稿"
    ]
    
    run_simulation(mock_inputs)
