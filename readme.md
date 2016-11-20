# shackie - asyncio based irc bot

## run

``` shell
docker-compose up -d
```


## run on armhf

``` shell
# redis
docker run -d --restart=always --name redis bobsense/redis-arm64
# build
docker build -f Dockerfile.armhf --tag=ircbot-build .
# run
docker run -d --link redis:redis --restart=always --name ircbot-run ircbot-build
```
