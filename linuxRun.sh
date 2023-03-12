docker build -t ainpc .
docker run -p 5502:5500 ainpc /bin/bash bootstrap.sh --name hi_asset_service
