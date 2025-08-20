docker-compose -f docker-compose-base.yml up mysql minio redis -d


docker-compose -f docker-compose-base.yml --profile elasticsearch up -d

docker-compose down

source .venv/bin/activate

./local_entrypoint.sh