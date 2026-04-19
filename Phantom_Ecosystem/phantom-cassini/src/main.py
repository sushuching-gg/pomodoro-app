import yaml
import sys
import os
import logging

# Add src to path just in case
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from interceptor import DataInterceptor
from advisor import ShadowAdvisor
from log_manager import LogManager
from skill_manager import SkillManager

# [GLOBAL] Use logging module instead of print()
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_simulation(inputs, test_draft_path=None):
    """
    Run the simulation loop.
    :param inputs: list of input strings
    :param test_draft_path: [P1] test draft file path, passed in by caller or CLI,
                            no longer hard-coded inside the function.
    """
    config_path = os.path.join('config', 'agent_config.yaml')
    config = load_config(config_path)

    log.info("=== Start: %s ===", config['system_persona']['name'])

    skill_manager = SkillManager(config)
    advisor       = ShadowAdvisor(config, skill_manager)
    interceptor   = DataInterceptor(config)
    # [P2] LogManager correctly initialised AND used inside the loop
    event_logger  = LogManager(config)

    log.info("--- Processing input stream ---")

    for raw_input in inputs:
        log.info(">> Input: %s", raw_input)

        # 1. Intercept and extract
        event_data = interceptor.extract_info(raw_input)

        # 2. Analyse and suggest
        suggestion = advisor.analyze_and_suggest(event_data)

        if suggestion:
            log.info("   [Shadow Suggestion] Trigger: %s", suggestion['trigger'])

            if suggestion.get('type') == 'SKILL_EXECUTION':
                skill  = suggestion['skill']
                script = suggestion['script']
                args   = suggestion['args']

                # [P1] Test path injected from outside, not hard-coded here
                if test_draft_path and ("Draft" in suggestion['trigger'][0] or "計畫書" in raw_input):
                    args = ["--draft", test_draft_path, "--type", "sports_tech"]

                log.info("      - Skill: %s -> %s", skill, script)
                log.info("      - Args: %s", args)

                result = skill_manager.run_skill(skill, script, args)
                log.info("      - Result:\n%s", result)

        # [P2] Actually write to log (was missing before)
        event_logger.append_log(event_data, suggestion)
        log.info("   -> Logged")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phantom Cassini Simulator")
    parser.add_argument("--input", "-i", nargs="+", default=["幫我檢查這份計畫書草稿"],
                        help="Input string(s)")
    # [P1] Draft path from CLI, not hard-coded
    parser.add_argument("--draft", default=None,
                        help="Test draft file path (optional, for testing only)")
    cli_args = parser.parse_args()
    run_simulation(cli_args.input, test_draft_path=cli_args.draft)
