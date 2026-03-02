import os
import subprocess
import sys
import logging

logger = logging.getLogger(__name__)

class SkillManager:
    """
    [M2] Auto-discovers skills from the skills/ directory.
    Each skill folder must contain a 'skill.yaml' manifest.
    No need to edit this file when adding a new skill - just drop the folder in.
    """

    MANIFEST_FILENAME = "skill.yaml"

    def __init__(self, config):
        self.config = config
        self.src_dir      = os.path.dirname(os.path.abspath(__file__))
        self.cassini_root = os.path.dirname(self.src_dir)
        self.skills_root  = os.path.normpath(os.path.join(self.cassini_root, "..", "skills"))
        # Auto-discover instead of hardcode
        self.skills = self._discover_skills()
        logger.info("[SkillManager] Discovered skills: %s", list(self.skills.keys()))

    def _discover_skills(self):
        """
        Scan skills_root for subdirectories that contain a skill.yaml manifest.
        Falls back to legacy hardcoded list if skills_root is missing or empty.
        """
        discovered = {}

        if not os.path.isdir(self.skills_root):
            logger.warning("[SkillManager] skills/ directory not found: %s", self.skills_root)
            return self._legacy_skills()

        for skill_name in os.listdir(self.skills_root):
            skill_path = os.path.join(self.skills_root, skill_name)
            if not os.path.isdir(skill_path):
                continue

            scripts_dir = os.path.join(skill_path, "scripts")
            if not os.path.isdir(scripts_dir):
                continue

            # Build scripts map from all .py files in scripts/
            scripts = {}
            for fname in os.listdir(scripts_dir):
                if fname.endswith(".py") and not fname.startswith("_"):
                    script_key = fname[:-3]  # strip .py
                    scripts[script_key] = os.path.join("scripts", fname)

            if scripts:
                discovered[skill_name] = {
                    "base_path": skill_path,
                    "scripts":   scripts,
                }

        return discovered if discovered else self._legacy_skills()

    def _legacy_skills(self):
        """Fallback: original hardcoded skill definitions."""
        logger.warning("[SkillManager] Using legacy hardcoded skill list as fallback.")
        return {
            "phantom-web-officer": {
                "base_path": os.path.join(self.skills_root, "phantom-web-officer"),
                "scripts":   {"plan_coach": "scripts/plan_coach.py", "execution_monitor": "scripts/execution_monitor.py"},
            },
            "phantom-policy-strategist": {
                "base_path": os.path.join(self.skills_root, "phantom-policy-strategist"),
                "scripts":   {"strategist": "scripts/strategist.py"},
            },
            "phantom-file-navigator": {
                "base_path": os.path.join(self.skills_root, "phantom-file-navigator"),
                "scripts":   {"navigator": "scripts/navigator.py", "opener": "scripts/opener.py"},
            },
        }

    def get_skill_script_path(self, skill_name, script_name):
        skill = self.skills.get(skill_name)
        if not skill:
            logger.warning("[SkillManager] Unknown skill: %s", skill_name)
            return None
        script_rel_path = skill["scripts"].get(script_name)
        if not script_rel_path:
            logger.warning("[SkillManager] Unknown script '%s' in skill '%s'", script_name, skill_name)
            return None
        return os.path.join(skill["base_path"], script_rel_path)

    def run_skill(self, skill_name, script_name, args):
        script_path = self.get_skill_script_path(skill_name, script_name)
        if not script_path:
            return "Error: Script path not resolved for {}/{}".format(skill_name, script_name)

        if not os.path.exists(script_path):
            return "Error: Script file not found at {}".format(script_path)

        command = [sys.executable, script_path] + args
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        logger.info("[SkillManager] Executing: %s", ' '.join(command))
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env,
                timeout=120,  # [P6] prevent single file from blocking indefinitely
            )
            output       = result.stdout.strip() if result.stdout else ""
            error_output = result.stderr.strip() if result.stderr else ""
            if result.returncode == 0:
                return output
            else:
                return "[Skill Execution Failed]\nError: {}\nOutput: {}".format(error_output, output)
        except subprocess.TimeoutExpired:
            logger.error("[SkillManager] Skill timed out: %s", script_path)
            return "[Timeout] Skill execution exceeded 120 seconds: {}".format(script_path)
        except Exception as e:
            return "[System Error] Failed to run skill: {}".format(str(e))
