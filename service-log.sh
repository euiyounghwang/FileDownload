

#!/bin/bash
set -e

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi

# tail -f ./logs/db-interface-restful-api.log
sudo journalctl -u filedownload_es_api.service -f