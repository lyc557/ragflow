https://ragflow.io/docs/dev/launch_ragflow_from_source

# 设置 HTTP/HTTPS 代理
export HTTP_PROXY="http://10.40.0.43:9666"
export HTTPS_PROXY="http://10.40.0.43:9666"

# 对于需要认证的代理
# 在环境中运行 UV
conda activate ragflow
uv sync --all-extras


# 在项目根目录
cd /Users/yangcailu/chengtay_code/ragflow

# 使用模块方式运行
python3 -m api.ragflow_server

source .venv/bin/activate

# 下载
   python download_deps.py --china-mirrors    # 使用中国镜像源下载（推荐国内用户）

export NLTK_DATA=/Users/yangcailu/chengtay_code/ragflow/nltk_data
# 安装 unixodbc
brew install unixodbc

# 激活虚拟环境
source .venv/bin/activate

# 使用 uv 同步依赖
uv sync