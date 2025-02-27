

#!/bin/bash
set -e

JAVA_HOME='C:\Users\euiyoung.hwang\'
PATH=$PATH:$JAVA_HOME
export JAVA_HOME

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

export PYTHONDONTWRITEBYTECODE=1

# -- background
#  sudo netstat -nlp | grep :8002
# nohup $SCRIPTDIR/service-start.sh &> /dev/null &

# gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:7091 --workers 4
# gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:7091 --workers 4 --timemot 120
python -m uvicorn main:app --reload --host=0.0.0.0 --port=7091 --workers 2
# poetry run uvicorn main:app --reload --host=0.0.0.0 --port=7091 --workers 4
