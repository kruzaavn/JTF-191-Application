#!/usr/bin/env sh

docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up -d
