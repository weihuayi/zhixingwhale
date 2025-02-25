"""
文本处理引擎
实现策略模式下的多种处理规则
"""
import re

class TextProcessor:
    def __init__(self, config):
        self.rules = config.get('replace_rules')
    
    def _replace_commands(self, text: str) -> str:
        """命令替换"""
        for src, tgt in self.rules['commands'].items():
            text = text.replace(src, tgt)
        return text
    
    def _replace_envs(self, text: str) -> str:
        """公式环境替换"""
        # 处理行内公式
        inline_start, inline_end, new_start, new_end = self.rules['inline']
        text = re.sub(
            f'{re.escape(inline_start)}(.*?){re.escape(inline_end)}',
            f'{new_start}\\1{new_end}',
            text
        )
        
        # 处理块公式
        display_start, display_end, _, _ = self.rules['display']
        text = re.sub(
            f'{re.escape(display_start)}(.*?){re.escape(display_end)}',
            f'{new_start}\\1{new_end}',
            text,
            flags=re.DOTALL
        )
        return text
    
    def process(self, text: str) -> str:
        """处理流水线"""
        text = self._replace_commands(text)
        text = self._replace_envs(text)
        return text
