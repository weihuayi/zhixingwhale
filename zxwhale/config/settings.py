"""
配置管理中心
实现配置加载与热更新功能
"""
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.default_config = {
            'auto_convert': True,
            'replace_rules': {
                'commands': {'\\mathbf': '\\bm'},
                'inline': ('\\(', '\\)', '$$', '$$'),
                'display': ('\\[', '\\]', '$$', '$$')
            },
            'check_interval': 1
        }
        self.config = self.default_config.copy()
    
    def load_from_file(self, config_path: str):
        """从文件加载配置"""
        if Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config.update(json.load(f))

    def get(self, key: str, default=None):
        return self.config.get(key, default)
