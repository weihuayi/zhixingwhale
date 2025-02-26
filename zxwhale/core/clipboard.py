"""
剪贴板监控服务（日志增强版）
实现观察者模式的核心逻辑，集成统一日志系统
"""
import pyperclip
import threading
import time
import logging
from typing import Callable, List

class ClipboardMonitor:
    def __init__(self, check_interval: float = 1.0):
        self.check_interval = check_interval
        self.observers: List[Callable[[str], None]] = []
        self._last_content = ""
        self._running = False
        self._thread = None
        
        # 初始化实例专属日志记录器
        self.logger = logging.getLogger(f"{__name__}.ClipboardMonitor")
        self.logger.propagate = True  # 启用向上传播
        self.logger.info(
            "初始化剪贴板监视器，检查间隔 %.1f秒", 
            self.check_interval
        )

    def add_observer(self, callback: Callable[[str], None]):
        """注册剪贴板更新回调（带安全审计）"""
        observer_name = callback.__name__ if hasattr(callback, '__name__') else 'Anonymous'
        self.logger.debug(
            "添加观察者: %s", 
            observer_name,
            extra={"observer_type": type(callback).__name__}  # 结构化日志
        )
        self.observers.append(callback)

    def start(self):
        """启动监控线程（带资源校验）"""
        if self._running:
            self.logger.warning("重复启动请求，当前状态: 运行中")
            return
            
        self._running = True
        self._thread = threading.Thread(
            target=self._monitor_loop, 
            daemon=True,
            name=f"ClipboardMonitorThread_{threading.get_ident()}"
        )
        self._thread.start()
        self.logger.info(
            "监控线程启动成功",
            extra={"thread_id": self._thread.ident}  # 线程追踪信息
        )

    def stop(self):
        """安全停止监控（带超时保护）"""
        if self._running:
            self.logger.info("停止请求已接收，等待线程退出...")
            self._running = False
            self._thread.join(timeout=5)
            if self._thread.is_alive():
                self.logger.error("线程停止超时，强制终止可能发生")
            else:
                self.logger.info("线程已安全停止")

    def _monitor_loop(self):
        self.logger.debug("监控循环启动")
        try:
            while self._running:
                self._check_clipboard()
                time.sleep(self.check_interval)
        except Exception as e:
            self.logger.exception(
                "监控循环异常终止: %s", 
                str(e),
                stack_info=True  # 记录完整堆栈
            )
        finally:
            self.logger.debug("监控循环退出")

    def _check_clipboard(self):
        try:
            current = pyperclip.paste()
            if current != self._last_content:
                content_length = len(current)
                self._last_content = current
                self.logger.info(
                    "剪贴板更新，长度: %d 字符", 
                    content_length,
                    extra={
                        "content_sample": current[:50] + ('...' if content_length >50 else '')  # 内容摘要
                    }
                )
                self._notify_observers(current)
        except pyperclip.PyperclipException as e:
            self.logger.error(
                "剪贴板访问错误: %s", 
                str(e),
                exc_info=True  # 包含异常对象信息
            )
            time.sleep(self.check_interval * 2)  # 错误时延长间隔

    def _notify_observers(self, content: str):
        self.logger.debug(
            "开始通知 %d 个观察者", 
            len(self.observers),
            extra={"observers_count": len(self.observers)}
        )
        
        for idx, callback in enumerate(self.observers):
            try:
                callback_name = callback.__name__ if hasattr(callback, '__name__') else f'Observer_{idx}'
                self.logger.debug("正在通知: %s", callback_name)
                callback(content)
            except Exception as e:
                self.logger.error(
                    "观察者执行失败: %s - %s",
                    callback_name,
                    str(e),
                    exc_info=True,
                    stack_info=True  # 记录调用堆栈
                )

if __name__ == "__main__":
    # 初始化日志系统（模拟主程序配置）
    from zxwhale.config import log_config
    log_config.setup_logging(level=logging.DEBUG)
    
    # 演示测试
    monitor = ClipboardMonitor(check_interval=0.5)
    
    def sample_callback(content: str):
        print(f"Callback received: {content[:20]}...")
    
    monitor.add_observer(sample_callback)
    
    try:
        monitor.start()
        print("监控运行中，尝试修改剪贴板内容...")
        time.sleep(3)
    finally:
        monitor.stop()
