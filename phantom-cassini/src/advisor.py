import re

class ShadowAdvisor:
    def __init__(self, config, skill_manager=None):
        self.config = config
        self.skill_manager = skill_manager
        self.triggers = config['core_instructions']['shadow_suggestions']['triggers']
        self.guardrails = config['guardrails']

    def analyze_and_suggest(self, event_data):
        """
        Analyzes the event and returns a suggestion block if triggers are met.
        """
        description = event_data['事件描述']
        
        # 1. Check for Skill Triggers (High Priority)
        if self.skill_manager:
            skill_action = self._check_skill_triggers(description)
            if skill_action:
                return skill_action

        # 2. Existing Keyword Triggers
        triggered_keywords = [original_kw for original_kw in self.triggers if original_kw in description]
        
        if not triggered_keywords:
            return None

        suggestion = {
            "trigger": triggered_keywords,
            "content": self._generate_advice(description, triggered_keywords)
        }
        
        # Check Guardrails
        if self._check_guardrails(description):
            suggestion['status'] = self.guardrails['approval_status_label']
        else:
            suggestion['status'] = "自動建議"
            
        return suggestion

    def _check_skill_triggers(self, text):
        # Define simple regex patterns for skills
        # Format: (Regex, SkillName, ScriptName, DefaultArgs)
        patterns = [
            (r"(計畫書|Draft).*(撰寫|寫|檢查|分析|Check|Analyze|Review)|(撰寫|寫|檢查|分析|Check|Analyze|Review).*(計畫書|Draft)", "phantom-web-officer", "plan_coach", ["--draft", "draft_v1.docx", "--type", "sports_tech"]),
            (r"(找|搜尋|Search).*(檔案|文件|File|需求書)", "phantom-file-navigator", "navigator", ["search"]),
            (r"(週報|月報|Report)", "phantom-web-officer", "execution_monitor", ["--report", "weekly_report.xlsx"]),
            (r"(政策|Policy).*(分析|Analyze)", "phantom-policy-strategist", "strategist", ["--plan", "policy_2026.docx", "--report", "exec_data.xlsx"])
        ]
        
        for pattern, skill, script, default_args in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Special handling for search to extract keywords
                final_args = default_args
                if skill == "phantom-file-navigator" and script == "navigator":
                    # Extract keywords from text
                    # Heuristic: Remove common verbs
                    clean_text = text
                    for stop_word in ["幫我", "找", "關於", "的", "檔案", "搜尋"]:
                         clean_text = clean_text.replace(stop_word, " ")
                    
                    query = clean_text.strip()
                    if not query:
                        query = text # Fallback
                        
                    final_args = ["search", query]

                return {
                    "trigger": [match.group(0)],
                    "type": "SKILL_EXECUTION",
                    "skill": skill,
                    "script": script,
                    "args": final_args,
                    "status": "技能執行"
                }
        return None

    def _generate_advice(self, description, keywords):
        advice = {}
        
        if "設備故障" in keywords:
            advice["現狀評估"] = "偵測到設施異常，可能影響實證數據完整性。"
            advice["建議對策"] = [
                "立即依照 SOP-2.1 啟動備用器材。",
                "通知維修廠商並記錄報修單號。"
            ]
            advice["預期影響"] = "若維修超過 24 小時，本週有效樣本數將減少 15%。"
            
        elif "負面情緒" in keywords:
            advice["現狀評估"] = "偵測到現場情緒波動，需防止客訴擴大。"
            advice["建議對策"] = [
                "啟動 SOP-2.2 關懷流程，移至安靜區對話。",
                "紀錄訴求但避免現場承諾具體補償。"
            ]
            advice["預期影響"] = "及時安撫可降低社群負評風險。"
            
        elif "進度延遲" in keywords:
             advice["現狀評估"] = "目前進度落後於預定時程。"
             advice["建議對策"] = [
                "盤點剩餘工作量，評估是否需加派人力。",
                "調整每日目標，優先完成核心指標。"
             ]
             advice["預期影響"] = "如不調整，專案驗收可能延誤。"

        return advice

    def _check_guardrails(self, text):
        """Returns True if approval is required"""
        restricted_keywords = self.guardrails['requires_approval_keywords']
        for kw in restricted_keywords:
            if kw in text:
                return True
        return False



