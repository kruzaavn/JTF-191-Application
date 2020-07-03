#!/usr/bin/env sh

docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml build
docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
