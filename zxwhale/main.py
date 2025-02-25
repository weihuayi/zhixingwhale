"""
程序入口文件
实现依赖注入和模块组装
"""
from config.settings import ConfigManager
from core.clipboard import ClipboardMonitor
from core.processor import TextProcessor
from ui.main_window import MainWindow

def bootstrap():
    # 初始化配置
    config = ConfigManager()
    config.load_from_file("config.json")  # 可选加载外部配置
    
    # 构建核心服务
    clip_monitor = ClipboardMonitor(config.get('check_interval', 1.0))
    text_processor = TextProcessor(config)
    
    # 启动界面
    window = MainWindow(clip_monitor, text_processor)
    clip_monitor.start()  # 启动剪贴板监控
    
    return window

if __name__ == "__main__":
    app = bootstrap()
    app.mainloop()
