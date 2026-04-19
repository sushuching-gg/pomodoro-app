import re

# [M4] Advice handlers: dict-of-functions replaces if/elif chain
# To add a new advice type: add a new entry here, no need to touch the main logic
ADVICE_HANDLERS = {
    "設備故障": lambda: {
        "現狀評估": "偵測到設施異常，可能影響實證數據完整性。",
        "建議對策": ["立即依照 SOP-2.1 啟動備用器材。", "通知維修廠商並記錄報修單號。"],
        "預期影響": "若維修超過 24 小時，本週有效樣本數將減少 15%。",
    },
    "負面情緒": lambda: {
        "現狀評估": "偵測到現場情緒波動，需防止客訴擴大。",
        "建議對策": ["啟動 SOP-2.2 關懷流程，移至安靜區對話。", "紀錄訴求但避免現場承諾具體補償。"],
        "預期影響": "及時安撫可降低社群負評風險。",
    },
    "進度延遲": lambda: {
        "現狀評估": "目前進度落後於預定時程。",
        "建議對策": ["盤點剩餘工作量，評估是否需加派人力。", "調整每日目標，優先完成核心指標。"],
        "預期影響": "如不調整，專案驗收可能延誤。",
    },
}

class ShadowAdvisor:
    def __init__(self, config, skill_manager=None):
        self.config        = config
        self.skill_manager = skill_manager
        self.triggers      = config['core_instructions']['shadow_suggestions']['triggers']
        self.guardrails    = config['guardrails']
        # [M1] Load skill trigger patterns from config instead of hardcoding in source
        self._skill_triggers = self._compile_skill_triggers(
            config.get('core_instructions', {}).get('skill_triggers', [])
        )

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _compile_skill_triggers(raw_triggers):
        """Pre-compile regex patterns from config for performance."""
        compiled = []
        for entry in raw_triggers:
            try:
                compiled.append({
                    "pattern":       re.compile(entry['pattern'], re.IGNORECASE),
                    "skill":         entry['skill'],
                    "script":        entry['script'],
                    "default_args":  entry.get('default_args', []),
                    "extract_query": entry.get('extract_query', False),
                })
            except re.error as e:
                print("[ShadowAdvisor] Invalid regex in config: {} - {}".format(entry.get('pattern'), e))
        return compiled

    # ── Public interface ─────────────────────────────────────────────────────

    def analyze_and_suggest(self, event_data):
        """Analyses the event and returns a suggestion block if triggers are met."""
        description = event_data['事件描述']

        # 1. Skill triggers (high priority, loaded from config [M1])
        if self.skill_manager:
            skill_action = self._check_skill_triggers(description)
            if skill_action:
                return skill_action

        # 2. Keyword-based shadow suggestions
        triggered_keywords = [kw for kw in self.triggers if kw in description]
        if not triggered_keywords:
            return None

        suggestion = {
            "trigger": triggered_keywords,
            "content": self._generate_advice(triggered_keywords),
        }
        suggestion['status'] = (
            self.guardrails['approval_status_label']
            if self._check_guardrails(description)
            else "自動建議"
        )
        return suggestion

    # ── Private methods ──────────────────────────────────────────────────────

    def _check_skill_triggers(self, text):
        """
        [M1] Check skill trigger patterns loaded from agent_config.yaml.
        No need to modify this method when adding new skills.
        """
        for entry in self._skill_triggers:
            match = entry["pattern"].search(text)
            if match:
                final_args = list(entry["default_args"])

                # Special handling: extract search query from text
                if entry.get("extract_query"):
                    clean = text
                    for stop in ["幫我", "找", "關於", "的", "檔案", "搜尋"]:
                        clean = clean.replace(stop, " ")
                    query = clean.strip() or text
                    final_args = ["search", query]

                return {
                    "trigger": [match.group(0)],
                    "type":    "SKILL_EXECUTION",
                    "skill":   entry["skill"],
                    "script":  entry["script"],
                    "args":    final_args,
                    "status":  "技能執行",
                }
        return None

    def _generate_advice(self, keywords):
        """
        [M4] Dict-of-handlers replaces if/elif chain.
        Returns advice for the first matched keyword.
        """
        for kw in keywords:
            handler = ADVICE_HANDLERS.get(kw)
            if handler:
                return handler()
        return {}

    def _check_guardrails(self, text):
        """Returns True if approval is required."""
        return any(kw in text for kw in self.guardrails['requires_approval_keywords'])
