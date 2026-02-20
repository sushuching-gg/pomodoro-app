import os
from datetime import datetime

class LogManager:
    def __init__(self, config):
        self.config = config
        self.output_path = config['knowledge_base']['output_log_path']
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        directory = os.path.dirname(self.output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        if not os.path.exists(self.output_path):
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write("| 時間 | 場域 | 處理狀態 | 事件描述 | 建議/備註 |\n")
                f.write("| --- | --- | --- | --- | --- |\n")

    def append_log(self, event_data, suggestion=None):
        """
        Appends a formatted row to the markdown log file.
        """
        time = event_data.get("時間", "")
        location = event_data.get("場域", "")
        status = event_data.get("處理狀態", "")
        description = event_data.get("事件描述", "").replace("\n", " ") # Keep single line for table
        
        note = ""
        if suggestion:
            status_tag = f"**{suggestion['status']}**" if suggestion.get('status') else ""
            note = f"{status_tag} {suggestion['content'].get('現狀評估', '')}"

        row = f"| {time} | {location} | {status} | {description} | {note} |\n"
        
        with open(self.output_path, 'a', encoding='utf-8') as f:
            f.write(row)
            
    def get_log_content(self):
        if os.path.exists(self.output_path):
            with open(self.output_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "Log file empty."
