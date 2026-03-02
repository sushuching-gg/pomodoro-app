import re
import difflib
from datetime import datetime

class DataInterceptor:
    def __init__(self, config):
        self.config = config
        locations_list = config['core_instructions']['semantic_correction']['known_locations']
        self.threshold = config['core_instructions']['semantic_correction']['threshold']
        # [P5] Convert to set for O(1) direct match; keep list for fuzzy fallback
        self._locations_set  = set(locations_list)
        self._locations_list = locations_list  # used only by get_close_matches

    def extract_info(self, text):
        """
        Extracts structured info from raw text.
        Simulates LLM extraction using Regex and heuristics for this demo.
        """
        result = {
            "時間":     self._extract_time(text),
            "場域":     self._extract_location(text),
            "事件描述": text.strip(),
            "處理狀態": self._determine_status(text),
        }
        return result

    def _extract_time(self, text):
        match = re.search(r'([0-1]?[0-9]|2[0-3]):([0-5][0-9])', text)
        if match:
            return match.group(0)
        return datetime.now().strftime("%H:%M")

    def _extract_location(self, text):
        """
        [P5] Two-stage lookup:
          1. O(1) set membership for direct match
          2. Only call get_close_matches() if direct match fails (expensive, avoid for every word)
        """
        words = text.split()
        for word in words:
            # Stage 1: direct set lookup  O(1)
            if word in self._locations_set:
                return word
        # Stage 2: fuzzy match only after all words fail direct lookup
        for word in words:
            matches = difflib.get_close_matches(word, self._locations_list, n=1, cutoff=self.threshold)
            if matches:
                return "{} (修正自: {})".format(matches[0], word)
        return "未知場域"

    def _determine_status(self, text):
        if "已解決" in text or "完成" in text:
            return "已解決"
        if "處理中" in text:
            return "處理中"
        return "待處理"
