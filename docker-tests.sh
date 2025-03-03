#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker run --rm -it --platform linux/amd64 -it -d \
  --name fn-filedownload-api-test --publish 7092:7092 --expose 7092 \
  --network bridge \
  -e ES_HOST=http://host.docker.internal:9200 \
  -v "$SCRIPTDIR:/app/FN-Basic-Services/" \
  fn-filedownload-api:test