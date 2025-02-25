"""
剪贴板监控服务
实现观察者模式的核心逻辑
"""
import pyperclip
import threading
import time
from typing import Callable, List

class ClipboardMonitor:
    def __init__(self, check_interval: float = 1.0):
        self.check_interval = check_interval
        self.observers: List[Callable[[str], None]] = []
        self._last_content = ""
        self._running = False

    def add_observer(self, callback: Callable[[str], None]):
        """注册剪贴板更新回调"""
        self.observers.append(callback)

    def start(self):
        """启动监控线程"""
        self._running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def _monitor_loop(self):
        while self._running:
            current = pyperclip.paste()
            if current != self._last_content:
                self._last_content = current
                for callback in self.observers:
                    callback(current)
            time.sleep(self.check_interval)
