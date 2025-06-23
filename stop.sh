#!/bin/sh

docker stop $(docker ps -q --filter name="wasp")
docker rm $(docker ps -q --filter name="wasp")
