"""
程序入口文件
实现依赖注入和模块组装
"""

from .config import setup_logging, ConfigManager
from .core.clipboard import ClipboardMonitor
from .core.processor import TextProcessor
from .ui.main_window import MainWindow

def bootstrap():
    # 初始化配置
    cm = ConfigManager()
    cm.load_from_file("./config/to_feishu.json")  # 可选加载外部配置
    
    # 构建核心服务
    clip_monitor = ClipboardMonitor(cm.get('check_interval', 1.0))
    text_processor = TextProcessor(cm.config)
    
    # 启动界面
    window = MainWindow(clip_monitor, text_processor)
    clip_monitor.start()  # 启动剪贴板监控
    
    return window

if __name__ == "__main__":
    setup_logging()
    app = bootstrap()
    app.mainloop()
