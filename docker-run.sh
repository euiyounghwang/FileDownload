#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker run --rm --platform linux/amd64 -it -d \
  --name fn-filedownload-api --publish 7091:7091 --expose 7091 \
  --network bridge \
  -e ES_HOST=http://host.docker.internal:9200 \
  -e KAFKA_HOST=host.docker.internal:29092,host.docker.internal:39092 \
  -e KAFKA_TOPIC=test-topic,test1-topic \
  -v "$SCRIPTDIR:/app/FN-Basic-Services/" \
  fn-filedownload-api:es