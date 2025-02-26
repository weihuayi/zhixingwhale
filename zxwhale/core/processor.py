"""
文本处理引擎
实现策略模式下的多种处理规则
"""
import re

class TextProcessor:
    def __init__(self, config):
        if 'replace_rules' not in config:
            raise KeyError("Missing required 'replace_rules' in config")
        self.rules = config['replace_rules']

    def _replace_commands(self, text: str) -> str:
        for src, tgt in self.rules['commands'].items():
            text = text.replace(src, tgt)
        return text

    def _replace_display_envs(self, text: str) -> str:
        display_start, display_end, new_start, new_end = self.rules['display']
        return re.sub(
            f'{re.escape(display_start)}(.*?){re.escape(display_end)}',
            f'{new_start}\\1{new_end}',
            text,
            flags=re.DOTALL
        )

    def _replace_inline_envs(self, text: str) -> str:
        inline_start, inline_end, new_start, new_end = self.rules['inline']
        return re.sub(
            f'{re.escape(inline_start)}(.*?){re.escape(inline_end)}',
            f'{new_start}\\1{new_end}',
            text
        )

    def process(self, text: str) -> str:
        text = self._replace_commands(text)
        text = self._replace_display_envs(text)
        text = self._replace_inline_envs(text)
        return text
