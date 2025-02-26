from setuptools import setup, find_packages
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).parent

# 读取README内容
with open(BASE_DIR / "README.md", encoding="utf-8") as f:
    long_description = f.read()

# 动态获取版本号
version = {}
with open(BASE_DIR / "zxwhale/__init__.py", encoding="utf-8") as f:
    exec(f.read(), version)

setup(
    name="zhixingwhale",
    version=version.get("__version__", "0.1.0"),
    author="Huayi Wei",
    author_email="weihuayi@xtu.edu.cn",
    description="智能办公助手 - 知行鲸灵",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weihuayi/zhixingwhale",
    packages=find_packages(
        exclude=["tests", "tests.*", "examples", "examples.*"]
    ),
    include_package_data=True,
    install_requires=[
        "pyperclip >= 1.8.2",
        "pillow >= 9.0.0"  # 若需要图形界面支持
    ],
    extras_require={
        "dev": [
            "pytest >= 7.0",
            "pytest-cov >= 4.0",
            "pytest-mock >= 3.10"
        ],
        "gui": [
            "tk >= 0.1.0"  # 基础GUI支持
        ]
    },
    entry_points={
        "console_scripts": [
            "zxwhale=zxwhale.main:bootstrap"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Office/Business",
        "Topic :: Utilities"
    ],
    keywords="AI assistant productivity automation",
    python_requires=">=3.8",
    project_urls={
#        "Documentation": "https://zhixingwhale.readthedocs.io",
        "Source": "https://github.com/yourusername/zhixingwhale",
        "Tracker": "https://github.com/yourusername/zhixingwhale/issues",
    },
)
