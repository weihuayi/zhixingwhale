"""
主界面实现
采用组合模式构建界面元素
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.clipboard import ClipboardMonitor
    from ..core.processor import TextProcessor

class MainWindow(tk.Tk):
    def __init__(self, clip_monitor: 'ClipboardMonitor', text_processor: 'TextProcessor'):
        super().__init__()
        self.title("知行鲸灵")
        self.geometry("800x600")
        
        self.clip_monitor = clip_monitor
        self.text_processor = text_processor
        
        self._init_ui()
        self._bind_events()
    
    def _init_ui(self):
        """界面初始化"""
        # 状态栏
        self.status_bar = ttk.Label(self, text="就绪", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 主功能区
        self.notebook = ttk.Notebook(self)
        self._create_basic_tab()
        self.notebook.pack(fill=tk.BOTH, expand=True)
    
    def _create_basic_tab(self):
        """创建基础功能标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="公式转换")
        
        # 三栏布局
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 源文本区
        self.src_text = scrolledtext.ScrolledText(paned, wrap=tk.WORD)
        paned.add(self.src_text, weight=2)
        
        # 操作按钮
        btn_frame = ttk.Frame(paned)
        ttk.Button(btn_frame, text="转换 →", command=self.on_process).pack(pady=10)
        paned.add(btn_frame, weight=0)
        
        # 结果区
        self.result_text = scrolledtext.ScrolledText(paned, wrap=tk.WORD)
        paned.add(self.result_text, weight=2)
    
    def _bind_events(self):
        """事件绑定"""
        self.clip_monitor.add_observer(self.update_source)
    
    def update_source(self, content: str):
        """更新源文本框内容"""
        self.src_text.delete(1.0, tk.END)
        self.src_text.insert(tk.END, content)
        self.status_bar.config(text="剪贴板内容已更新")
    
    def on_process(self):
        """处理按钮回调"""
        raw_text = self.src_text.get(1.0, tk.END)
        processed = self.text_processor.process(raw_text)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, processed)
        self.status_bar.config(text="处理完成")
