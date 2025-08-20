#!/usr/bin/env bash

set -e

# 设置本地路径 - 获取项目根目录（docker目录的上级目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONF_DIR="${PROJECT_ROOT}/conf"
TEMPLATE_FILE="${SCRIPT_DIR}/service_conf.yaml.template"
CONF_FILE="${CONF_DIR}/service_conf.yaml"

echo "项目根目录: ${PROJECT_ROOT}"
echo "模板文件: ${TEMPLATE_FILE}"
echo "配置文件: ${CONF_FILE}"

# 检查模板文件是否存在
if [[ ! -f "${TEMPLATE_FILE}" ]]; then
    echo "错误: 模板文件不存在: ${TEMPLATE_FILE}"
    exit 1
fi

# 确保配置目录存在
mkdir -p "${CONF_DIR}"

# 设置默认环境变量（如果未设置）
export RAGFLOW_HOST=${RAGFLOW_HOST:-0.0.0.0}
export MYSQL_DBNAME=${MYSQL_DBNAME:-rag_flow}
export MYSQL_USER=${MYSQL_USER:-root}
export MYSQL_PASSWORD=${MYSQL_PASSWORD:-infini_rag_flow}
export MYSQL_HOST=${MYSQL_HOST:-localhost}
export MINIO_USER=${MINIO_USER:-rag_flow}
export MINIO_PASSWORD=${MINIO_PASSWORD:-infini_rag_flow}
export MINIO_HOST=${MINIO_HOST:-localhost}
export ES_HOST=${ES_HOST:-localhost}
export ES_USER=${ES_USER:-elastic}
export ELASTIC_PASSWORD=${ELASTIC_PASSWORD:-infini_rag_flow}
export REDIS_PASSWORD=${REDIS_PASSWORD:-infini_rag_flow}
export REDIS_HOST=${REDIS_HOST:-localhost}
export INFINITY_HOST=${INFINITY_HOST:-localhost}

# 生成配置文件
echo "生成配置文件..."
rm -f "${CONF_FILE}"
while IFS= read -r line || [[ -n "$line" ]]; do
    eval "echo \"$line\"" >> "${CONF_FILE}"
done < "${TEMPLATE_FILE}"

echo "配置文件已生成: ${CONF_FILE}"

# 设置环境变量
export LD_LIBRARY_PATH="/usr/local/lib:/usr/lib"
# 关键修复：设置PYTHONPATH包含项目根目录
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"
PY=python3

# 切换到项目根目录
cd "${PROJECT_ROOT}"

# 检查 Python 服务器文件是否存在
if [[ ! -f "api/ragflow_server.py" ]]; then
    echo "错误: Python 服务器文件不存在: ${PROJECT_ROOT}/api/ragflow_server.py"
    echo "请确保您在正确的项目目录中运行此脚本"
    exit 1
fi

# 启动 RAGFlow 服务器
echo "启动 RAGFlow 服务器..."
echo "当前工作目录: $(pwd)"
echo "PYTHONPATH: ${PYTHONPATH}"
while true; do
    "$PY" api/ragflow_server.py
done