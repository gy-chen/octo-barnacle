docker build -t octo-barnacle:build . -f Dockerfile.build
docker container create --name extract octo-barnacle:build
docker container cp extract:/app/dist ./dist
docker container rm -f extract
docker build --no-cache -t octo-barnacle:mark-spa .