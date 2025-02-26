import pytest
from zxwhale.core.processor import TextProcessor

@pytest.fixture
def sample_config():
    return {
        'replace_rules': {
            'commands': {'\\mathbf': '\\bm'},
            'inline': ('\\(', '\\)', '$$', '$$'),
            'display': ('\\[', '\\]', '$$', '$$')
        }
    }

@pytest.fixture
def processor(sample_config):
    return TextProcessor(sample_config)

class TestTextProcessor:
    @pytest.mark.parametrize("input_text, expected", [
        (r"\mathbf{A}", r"\bm{A}"),
        (r"行内公式 \(a^2 + b^2 = c^2\) 结束", r"行内公式 $$a^2 + b^2 = c^2$$ 结束"),
        (r"\[ \int x dx \]", r"$$ \int x dx $$"),
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

    def test_multiline_flag(self, processor):
        input_text = r"\[a\nb\]"
        expected = r"$$a\nb$$"
        assert processor.process(input_text) == expected

    def test_empty_input(self, processor):
        assert processor.process("") == ""

    def test_invalid_config(self):
        with pytest.raises(KeyError):
            TextProcessor({"invalid": "config"})
