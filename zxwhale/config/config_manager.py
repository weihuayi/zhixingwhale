# config_manager.py
"""
配置管理中心 V2
集成统一日志配置，实现日志功能解耦
"""
import json
from pathlib import Path
import logging
from . import log_config  # 新增导入

class ConfigManager:
    def __init__(self):
        self.config = {}
        # 继承log_config的配置
        self.logger = logging.getLogger(__name__)  # 关键变更[7](@ref)
        self.logger.propagate = True  # 允许传播到根记录器[5](@ref)
        
    def load_from_file(self, config_path: str):
        """集成统一日志的加载方法"""
        self.logger.info(f"启动配置文件加载流程：{config_path}")
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                self.logger.error(f"配置文件路径不可达：{config_path}")
                return False
                
            with open(config_file, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
                self.logger.info(
                    f"加载完成，新增{len(loaded_config)}项配置",
                    extra={"config_file": config_path}  # 结构化日志[6](@ref)
                )
                return True
        except json.JSONDecodeError as e:
            self.logger.exception("配置文件解析异常，请检查JSON格式", exc_info=e)
        except Exception as e:
            self.logger.error(
                "未知加载错误",
                exc_info=e,
                stack_info=True  # 记录堆栈信息[7](@ref)
            )
        return False

    def get(self, key: str, default=None):
        value = self.config.get(key, default)
        self.logger.debug(f"访问配置项 {key} => {str(value)[:50]}")  # 防止敏感信息泄露[5](@ref)
        return value

# config_manager.py (续)
if __name__ == "__main__":
    # 初始化日志系统
    log_config.setup_logging()  # 关键变更[5](@ref)
    
    # 演示用例
    cm = ConfigManager()
    test_file = "to_feishu.json"
    
    if cm.load_from_file(test_file):
        print("\n配置项测试：")
        print("auto_convert ->", cm.get("auto_convert"))
        print("check_interval ->", cm.get("check_interval"))
        print("未定义项测试 ->", cm.get("undefined_key", "默认值"))
    else:
        print("!! 配置加载失败，请检查错误日志")
