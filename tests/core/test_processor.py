import pytest
from zxwhale.core.processor import TextProcessor

@pytest.fixture
def sample_config():
    return {
        'replace_rules': {
            'commands': {
                '\\mathbf': '\\bm',
            },
            'inline': ('\\(', '\\)', '$$', '$$'),
            'display': ('\\[', '\\]', '$$', '$$')
        }
    }

@pytest.fixture
def processor(sample_config):
    return TextProcessor(sample_config)

class TestTextProcessor:
    """测试文本处理引擎"""
    
    @pytest.mark.parametrize("input_text, expected", [
        # 命令替换测试
        (r"\mathbf{A}", r"\bm{A}"),
        # 混合命令替换
        (r"\mathbf{\mathbb{Q}}", r"\bm{\Bbb{Q}}"),
        # 行内公式替换
        (r"行内公式 \(a^2 + b^2 = c^2\) 结束", r"行内公式 $$a^2 + b^2 = c^2$$ 结束"),
        # 块公式替换
        (r"\[ \int x dx \]", r"$$ \int x dx $$"),
        # 嵌套内容处理
        (
            r"\mathbf{变量}在\(\mathbf{矩阵}\)中:\n\\[ \mathbf{X} = \mathbb{R}^{n} \\]",
            r"\bm{变量}在$$\bm{矩阵}$$中:\n$$ \bm{X} = \Bbb{R}^{n} $$"
        )
    ])
    def test_process(self, processor, input_text, expected):
        assert processor.process(input_text) == expected
    
    def test_display_math_multiline(self, processor):
        input_text = r"""多行公式：
\[
\begin{matrix}
a & b \\
c & d
\end{matrix}
\]"""
        expected = r"""多行公式：
$$
\begin{matrix}
a & b \\
c & d
\end{matrix}
$$"""
        assert processor.process(input_text) == expected
    
    def test_empty_input(self, processor):
        assert processor.process("") == ""
