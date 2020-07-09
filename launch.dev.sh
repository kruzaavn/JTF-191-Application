#!/usr/bin/env sh

docker-compose -f docker-compose.yaml up -d --build

docker-compose stop ui