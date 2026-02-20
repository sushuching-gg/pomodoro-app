import re
import difflib
from datetime import datetime

class DataInterceptor:
    def __init__(self, config):
        self.config = config
        self.known_locations = config['core_instructions']['semantic_correction']['known_locations']
        self.threshold = config['core_instructions']['semantic_correction']['threshold']

    def extract_info(self, text):
        """
        Extracts structured info from raw text. 
        Simulates LLM extraction using Regex and heuristics for this demo.
        """
        result = {
            "時間": self._extract_time(text),
            "場域": self._extract_location(text),
            "事件描述": text.strip(),
            "處理狀態": self._determine_status(text)
        }
        return result

    def _extract_time(self, text):
        # Regex to find time patterns like 14:30, 2pm, etc.
        match = re.search(r'([0-1]?[0-9]|2[0-3]):([0-5][0-9])', text)
        if match:
            return match.group(0)
        return datetime.now().strftime("%H:%M") # Default to current time if not found

    def _extract_location(self, text):
        # Check against known locations with fuzzy matching
        words = text.split()
        for word in words:
            # Direct match
            if word in self.known_locations:
                return word
            
            # Fuzzy match
            matches = difflib.get_close_matches(word, self.known_locations, n=1, cutoff=self.threshold)
            if matches:
                return f"{matches[0]} (修正自: {word})"
        
        return "未知場域"

    def _determine_status(self, text):
        if "已解決" in text or "完成" in text:
            return "已解決"
        if "處理中" in text:
            return "處理中"
        return "待處理"
