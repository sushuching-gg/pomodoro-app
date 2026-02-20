import os
import subprocess
import json
import sys

class SkillManager:
    def __init__(self, config):
        self.config = config
        self.src_dir = os.path.dirname(os.path.abspath(__file__))
        self.cassini_root = os.path.dirname(self.src_dir)
        self.skills_root = os.path.join(self.cassini_root, "..", "skills")
        
        self.skills = {
            "phantom-web-officer": {
                "base_path": os.path.join(self.skills_root, "phantom-web-officer"),
                "scripts": {
                    "plan_coach": "scripts/plan_coach.py",
                    "execution_monitor": "scripts/execution_monitor.py"
                }
            },
            "phantom-policy-strategist": {
                "base_path": os.path.join(self.skills_root, "phantom-policy-strategist"),
                "scripts": {
                    "strategist": "scripts/strategist.py"
                }
            },
            "phantom-file-navigator": {
                "base_path": os.path.join(self.skills_root, "phantom-file-navigator"),
                "scripts": {
                    "navigator": "scripts/navigator.py",
                    "opener": "scripts/opener.py"
                }
            }
        }

    def get_skill_script_path(self, skill_name, script_name):
        skill = self.skills.get(skill_name)
        if not skill:
            return None
        script_rel_path = skill["scripts"].get(script_name)
        if not script_rel_path:
             return None
        return os.path.join(skill["base_path"], script_rel_path)

    def run_skill(self, skill_name, script_name, args):
        script_path = self.get_skill_script_path(skill_name, script_name)
        if not script_path:
            return f"Error: Script path not resolved for {skill_name}/{script_name}"
        
        if not os.path.exists(script_path):
            return f"Error: Script file not found at {script_path}"

        command = [sys.executable, script_path] + args
        
        # Prepare environment with UTF-8 encoding for IO
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        print(f"[SkillManager] Executing: {' '.join(command)}")

        try:
            # Use errors='replace' to avoid crashing on decoding errors
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                errors='replace',
                env=env
            )
            
            output = result.stdout.strip() if result.stdout else ""
            error_output = result.stderr.strip() if result.stderr else ""

            if result.returncode == 0:
                return output
            else:
                return f"[Skill Execution Failed]\nError: {error_output}\nOutput: {output}"
        except Exception as e:
            return f"[System Error] Failed to run skill: {str(e)}"
