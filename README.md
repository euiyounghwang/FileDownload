# FileDownload
<i> FileDownload

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python.
This is a repository that provides to upload file via user interface(`http://localhost:7091/ui`) and download them using the endpoint(`http://localhost:7091/filelist`,`http://localhost:7091/download/<file>`).


### Install Poerty
```
https://python-poetry.org/docs/?ref=dylancastillo.co#installing-with-the-official-installer
```


### Using Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
```


### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
- Please install the package `pip install poetry` first before installing poetry add any libraries
```bash
poetry config virtualenvs.in-project true
poetry init
poetry add fastapi
poetry add uvicorn
poetry add gunicorn
poetry add pytz
poetry add httpx
poetry add pytest
poetry add pytest-cov
poetry add requests
poetry add python-dotenv
```

or you can run this shell script `./create_virtual_env.sh` to make an environment. then go to virtual enviroment using `source .venv/bin/activate`



### Register Service
- sudo service filedownload_es_api status/stop/start/restart
```bash
#-- sudo vi /etc/systemd/system/filedownload_es_api.service
[Unit]
Description=FileDownload ES Service

[Service]
User=devuser
Group=devuser
Type=simple
ExecStart=/bin/bash /home/devuser/filedownload_es_api/service-start.sh
ExecStop= /usr/bin/killall filedownload_es_api

[Install]
WantedBy=default.target


# Service command
sudo systemctl daemon-reload 
sudo systemctl enable filedownload_es_api.service
sudo systemctl start filedownload_es_api.service 
sudo systemctl status filedownload_es_api.service 
sudo systemctl stop filedownload_es_api.service 

sudo service filedownload_es_api status/stop/start
```


### Service
- Run this command `./start-start.sh` or python -m uvicorn main:app --reload --host=0.0.0.0 --port=7091 --workers 1
- Service : `http://localhost:7091/docs`
```bash
source .venv/bin/activate
(.venv) ➜  FileDownload git:(master) ✗ ./service_start.sh
ciated with a value
WARNING:  StatReload detected changes in 'main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [14128]
INFO:     Started server process [30808]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61531 - "GET /filelist HTTP/1.1" 200 OK
```


### Pytest
- Reference : https://velog.io/@sangyeon217/pytest-execution
- Go to virtual enviroment using `source .venv/bin/activate`
- Run this command manually: `poetry run py.test -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/` or `./pytest.sh`
- Run pytest with all test_* files : `source .venv/bin/activate` - `python -m pytest ./tests/`
- Run pytest with a particular function : `source .venv/bin/activate` - `pytest -v ./tests/test_api.py -k test_api` or `pytest -sv ./tests/test_api.py -k test_api`
```bash
$ pytest -sv ./tests/test_api.py -k test_api
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.3.4, pluggy-1.5.0 -- C:\Users\euiyoung.hwang\Git_Workspace\FileDownload\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\euiyoung.hwang\Git_Workspace\FileDownload\tests
configfile: pytest.ini
plugins: anyio-4.8.0, cov-6.0.0
collecting ... collected 2 items

tests\test_api.py::test_skip SKIPPED (no way of currently testing this)
tests\test_api.py::test_api [2025-02-27 14:26:56,087] [INFO] [_client] [_send_single_request] HTTP Request: GET http://testserver/ "HTTP/1.1 200 OK"
PASSED                
```