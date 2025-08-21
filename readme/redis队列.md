# 连接到 Redis 容器
docker exec -it ragflow-redis redis-cli
docker exec -it ragflow-redis redis-cli -a infini_rag_flow
# 创建队列组（需要先有消息在队列中）
XGROUP CREATE rag_flow_svr_queue rag_flow_svr_task_broker 0 MKSTREAM
REDIS_PASSWORD=infini_rag_flow

# 检查 Redis 容器状态
docker ps | grep redis

# 检查队列信息
docker exec -it ragflow-redis redis-cli XINFO GROUPS rag_flow_svr_queue

uv add torch torchvision torchaudio

# 或者同步所有依赖
uv sync

uv add FlagEmbedding