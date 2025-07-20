#!/usr/bin/env python3

"""
RAGFlow 依赖下载脚本

本脚本用于下载 RAGFlow 项目运行所需的各种依赖和模型文件，包括：

1. HuggingFace 模型:
   - InfiniFlow/text_concat_xgb_v1.0: 文本拼接 XGBoost 模型，用于文本处理和分类
   - InfiniFlow/deepdoc: 深度文档处理模型，用于文档解析和理解
   - InfiniFlow/huqie: 中文分词模型，用于中文文本分词处理
   - BAAI/bge-large-zh-v1.5: 北京智源研究院的中文大型嵌入模型，用于文本向量化
   - maidalun1020/bce-embedding-base_v1: BCE 基础嵌入模型，用于文本嵌入

2. 系统依赖:
   - libssl1.1: OpenSSL 加密库（支持 amd64 和 arm64 架构）
   - tika-server-standard-3.0.0.jar: Apache Tika 服务器，用于提取各种文档格式的内容
   - cl100k_base.tiktoken: OpenAI 的 tokenizer 编码文件，用于文本分词
   - Chrome 浏览器和 ChromeDriver: 用于网页内容爬取和自动化操作

3. NLTK 自然语言处理数据:
   - wordnet: 英语词汇语义网络数据库
   - punkt: 句子边界检测模型
   - punkt_tab: 句子分割器的表格化数据

使用方法:
   python download_deps.py                    # 使用默认源下载
   python download_deps.py --china-mirrors    # 使用中国镜像源下载（推荐国内用户）

注意: 使用 --china-mirrors 参数可以显著提高国内用户的下载速度和成功率。
"""

# PEP 723 metadata
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "huggingface-hub",
#   "nltk",
#   "argparse",
# ]
# ///

from huggingface_hub import snapshot_download
from typing import Union
import nltk
import os
import urllib.request
import argparse

def get_urls(use_china_mirrors=False) -> Union[str, list[str]]:
    """
    获取下载链接列表
    
    Args:
        use_china_mirrors (bool): 是否使用中国镜像源
        
    Returns:
        list: 包含下载链接的列表，支持字符串或 [url, filename] 格式
    """
    if use_china_mirrors:
        return [
            "http://mirrors.tuna.tsinghua.edu.cn/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb",
            "http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_arm64.deb",
            "https://repo.huaweicloud.com/repository/maven/org/apache/tika/tika-server-standard/3.0.0/tika-server-standard-3.0.0.jar",
            "https://repo.huaweicloud.com/repository/maven/org/apache/tika/tika-server-standard/3.0.0/tika-server-standard-3.0.0.jar.md5",
            "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken",
            ["https://registry.npmmirror.com/-/binary/chrome-for-testing/121.0.6167.85/linux64/chrome-linux64.zip", "chrome-linux64-121-0-6167-85"],
            ["https://registry.npmmirror.com/-/binary/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip", "chromedriver-linux64-121-0-6167-85"],
        ]
    else:
        return [
            "http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb",
            "http://ports.ubuntu.com/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_arm64.deb",
            "https://repo1.maven.org/maven2/org/apache/tika/tika-server-standard/3.0.0/tika-server-standard-3.0.0.jar",
            "https://repo1.maven.org/maven2/org/apache/tika/tika-server-standard/3.0.0/tika-server-standard-3.0.0.jar.md5",
            "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken",
            "https://storage.googleapis.com/chrome-for-testing-public/121.0.6167.85/linux64/chrome-linux64.zip",
            "https://storage.googleapis.com/chrome-for-testing-public/121.0.6167.85/linux64/chromedriver-linux64.zip",
        ]

# HuggingFace 模型仓库列表
repos = [
    "InfiniFlow/text_concat_xgb_v1.0",      # 文本拼接 XGBoost 模型
    "InfiniFlow/deepdoc",                   # 深度文档处理模型
    "InfiniFlow/huqie",                     # 中文分词模型
    "BAAI/bge-large-zh-v1.5",              # 中文大型嵌入模型
    "maidalun1020/bce-embedding-base_v1",   # BCE 基础嵌入模型
]

def download_model(repo_id):
    """
    从 HuggingFace 下载模型
    
    Args:
        repo_id (str): HuggingFace 模型仓库 ID
    """
    local_dir = os.path.abspath(os.path.join("huggingface.co", repo_id))
    os.makedirs(local_dir, exist_ok=True)
    snapshot_download(repo_id=repo_id, local_dir=local_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download dependencies with optional China mirror support')
    parser.add_argument('--china-mirrors', action='store_true', help='Use China-accessible mirrors for downloads')
    args = parser.parse_args()
    
    urls = get_urls(args.china_mirrors)
    
    # 下载系统依赖文件
    for url in urls:
        download_url = url[0] if isinstance(url, list) else url
        filename = url[1] if isinstance(url, list) else url.split("/")[-1]
        print(f"Downloading {filename} from {download_url}...")
        if not os.path.exists(filename):
            urllib.request.urlretrieve(download_url, filename)

    # 下载 NLTK 数据
    local_dir = os.path.abspath('nltk_data')
    for data in ['wordnet', 'punkt', 'punkt_tab']:
        print(f"Downloading nltk {data}...")
        nltk.download(data, download_dir=local_dir)

    # 下载 HuggingFace 模型
    for repo_id in repos:
        print(f"Downloading huggingface repo {repo_id}...")
        download_model(repo_id)
