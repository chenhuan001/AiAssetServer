docker build -t ai_asset_server .
docker run -p 5503:5500 -it ai_asset_server /bin/bash bootstrap.sh