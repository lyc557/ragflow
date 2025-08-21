docker-compose -f docker-compose-base.yml up mysql minio redis -d


docker-compose -f docker-compose-base.yml --profile elasticsearch up -d

docker-compose down

source .venv/bin/activate
export HF_ENDPOINT=https://hf-mirror.com
./docker/local_entrypoint.sh


# 前端启动

cd web
npm install
npm run dev


pkill -f "ragflow_server.py|task_executor.py"