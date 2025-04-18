export STORAGE_LOCATION=$HOME/anythingllm
mkdir -p $STORAGE_LOCATION
touch "$STORAGE_LOCATION/.env"

docker run --restart always -p 3001:3001 \
	--add-host=host.docker.internal:192.168.0.2 --net=host \
	--cap-add SYS_ADMIN \
	-v ${STORAGE_LOCATION}:/app/server/storage \
	-v ${STORAGE_LOCATION}/.env:/app/server/.env \
	-e STORAGE_DIR="/app/server/storage" \
	--name anythingllm \
	mintplexlabs/anythingllm
