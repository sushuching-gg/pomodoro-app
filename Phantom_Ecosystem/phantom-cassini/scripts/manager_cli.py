import argparse
import sys
import os
import yaml

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # phantom-cassini root
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)

# Change CWD to project_root so relative paths in config work
os.chdir(project_root)

# Correct import
def load_config():
    config_path = os.path.join(project_root, 'config', 'agent_config.yaml')
    if not os.path.exists(config_path):
        print(f"錯誤: 找不到設定檔 {config_path}")
        sys.exit(1)
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

try:
    from interceptor import DataInterceptor
    from advisor import ShadowAdvisor
    from log_manager import LogManager
    from report_generator import ReportGenerator
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def handle_log(args):
    config = load_config()
    interceptor = DataInterceptor(config)
    advisor = ShadowAdvisor(config)
    logger = LogManager(config)

    raw_input = args.message
    print(f">> 接收輸入: {raw_input}")

    event_data = interceptor.extract_info(raw_input)
    print(f"   [提取結果] 時間:{event_data['時間']} | 場域:{event_data['場域']} | 狀態:{event_data['處理狀態']}")

    suggestion = advisor.analyze_and_suggest(event_data)
    if suggestion:
        print(f"   [影子建議] !!! 觸發條件: {suggestion['trigger']} !!!")
        print(f"   狀態: {suggestion['status']}")
        content = suggestion['content']
        print(f"      - 評估: {content.get('現狀評估')}")
        print(f"      - 對策: {content.get('建議對策')}")
    
    logger.append_log(event_data, suggestion)
    print("   -> 已寫入日誌")

def handle_report(args):
    config = load_config()
    reporter = ReportGenerator(config)
    
    result = reporter.generate_report()
    if result:
        print(f"週報生成於: {result}")

def main():
    parser = argparse.ArgumentParser(description="Phantom Manager CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    log_parser = subparsers.add_parser('log', help='Log an event')
    log_parser.add_argument('message', type=str, help='The event message to log')

    report_parser = subparsers.add_parser('report', help='Generate weekly report')

    args = parser.parse_args()

    if args.command == 'log':
        handle_log(args)
    elif args.command == 'report':
        handle_report(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
