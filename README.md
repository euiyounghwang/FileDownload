# FileDownload
<i> FileDownload

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python.
This is a repository that provides to deliver the records to the Prometheus-Export application.


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
#-- /etc/systemd/system/filedownload_es_api.service
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
