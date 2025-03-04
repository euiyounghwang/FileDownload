
from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
# from controller import db_controller
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import shutil
from fastapi.staticfiles import StaticFiles
# from dotenv import load_dotenv
import shutil
import os
from injector import logger
import bcrypt
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



host = os.getenv("HOST")
# directory = r'C://Users/euiyoung.hwang/Git_Workspace/FileDownload'
directory = os.getenv("FILE_DIR")


app = APIRouter(
    prefix="/elk",
)


@app.get("/user_password_bcrypt", 
          status_code=200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/elk/user_password_bcrypt?plain_text_password=test", 
          summary="Cluster Info")
async def user_password_bcrypt(plain_text_password="test"):
    ''' encrypt'''
    try:
        logger.info(f"user_password_bcrypt called : {plain_text_password}")
        '''
        # Generating Salt
        salt = bcrypt.gensalt(10)

        # Hashing Password
        hash_password = bcrypt.hashpw(
            password=plain_text_password,
            salt=salt
        )
        
        print(f"Actual Password: {plain_text_password.decode('utf-8')}")
        # Print Hashed Password
        print(f"Hashed Password: {hash_password.decode('utf-8')}")

        return hash_password
        '''
        return {
            "Actual_Password" : plain_text_password,
            "Hashed_Password" : pwd_context.hash(plain_text_password)
        }
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})


@app.get("/ui", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <head>
            <title>FileDownload Service - Upload File</title>
            <link rel="shortcut icon" href="http://%s:7091/static/image/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <h1>The ES Team Service - Upload File with Extra Fields</h1>
            <form action="/elk/uploadfile/" method="post" enctype="multipart/form-data">
                <input type="file" name="file"><br>
                <input type="text" name="item_id" placeholder="Item ID"><br>
                <input type="text" name="description" placeholder="Description"><br>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """ % (host)



@app.get("/xpack_admin", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <head>
            <title>FileDownload Service - Upload File</title>
            <style type='text/css'>
                p { font-size: 19px;}
                li {
                    font-size: 18px; line-height: 2em;
                }
            </style>
            <link rel="shortcut icon" href="http://%s:7091/static/image/favicon.ico" type="image/x-icon">

        </head>
        <body>
            <h1>The ES Team Service - Download CA certification file for the upgraded Elasticsearch v.8.17.0 with search guard as x-pack</h1>
            <p>Root CA (Certificate Authority) is a certificate that will be used to sign all other certificates within a system. In other words, Root CA is an issuer of node, client and admin certificates.
             A CA certificate is a digital certificate issued by a certificate authority (CA), so SSL clients (such as web browsers) can use it to verify the SSL certificates sign by this CA.
            <BR/><BR/>
            The csr mode generates certificate signing requests (CSRs) that You can send to a trusted certificate authority to obtain signed certificates. The signed certificates must be in PEM format to work with Elasticsearch security features.
            </p>
            <ul>
            <li><b>DEV Environment</b></li>
			<li><b>QA Environment</b></li>
            <ol>
				<li><a href="http://%s:7091/elk/download/qa13-es8-ca.pem">QA-13 CA certificate</a></li>
			</ol>
            <li><b>PROD Environment</b></li>
	    	</ul>
        </body>
    </html>
    """ % (host, host)


@app.get("/xpack", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <head>
            <title>FileDownload Service - Upload File</title>
            <style type='text/css'>
                p { font-size: 19px;}
                li {
                    font-size: 18px; line-height: 2em;
                }
            </style>
            <link rel="shortcut icon" href="http://%s:7091/static/image/favicon.ico" type="image/x-icon">

        </head>
        <body>
            <h1>The ES Team Service - Download CA certification file for the upgraded Elasticsearch v.8.17.0 with search guard as x-pack</h1>
            <p>A CA certificate is a digital certificate issued by a certificate authority (CA), so SSL clients (such as web browsers) can use it to verify the SSL certificates sign by this CA.</p>
            <ul>
            <li><b>DEV Environment</b></li>
			<li><b>QA Environment</b></li>
            <ol>
				<li><a href="http://%s:7091/elk/download/qa13-es8-ca.pem">QA-13 CA certificate</a></li>
			</ol>
            <li><b>PROD Environment</b></li>
	    	</ul>
        </body>
    </html>
    """ % (host, host)


@app.get("/on_call", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <head>
            <title>On_Call - Stop/Start the middleware ES/Kafka/Spark Services</title>
            <style type='text/css'>
                p { font-size: 19px;}
                li {
                    font-size: 18px; line-height: 2em;
                }
            </style>
            <link rel="shortcut icon" href="http://%s:7091/static/image/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <h1>Stop/Start the middleware ES/Kafka/Spark Services</h1>
            <p><b>Stop Services</b></p>
            <ul>
                <li><b>Stop Spark custom job</b></li>
                <ol>
                    <li>http://localhost:8080/ (kill click for jobs)</li>
                </ol>
                <li><b>Stop Spark Cluster.</b></li>
                <ol>
                    <li>sudo su -l %s</li>
                    <li><b><mark>[%s] /apps/spark/latest/sbin/stop-all.sh</mark></b></li>
                    <li>[others] /apps/spark-2.2.0-bin-hadoop2.7/sbin/stop-all.sh</li>
                </ol>
                <li><b>Pause OM/WM listeners.</b></li>
                <li><b>Stop Kafka Connect – all 3 nodes.</b></li>
                <ol>
                    <li>sudo utils/connectUtil.sh status</li>
                    <li>sudo utils/connectUtil.sh stop</li>
                    <li>sudo netstat -nlp | grep :8083</li>
                    <li>curl -XGET 'localhost:8083/connectors' | jq</li>
                    <li>curl -XGET 'localhost:8083/connectors/epq_wmxd_jdbc/status' | jq</li>
                    <li>curl -XGET 'localhost:8083/connectors/epq_omxd_jdbc/status' | jq</li>
                </ol>
                <li><b>Stop Kafka/ZooKeeper – all 3 nodes.</b></li>
                <ol>
                    <li>sudo utils/kafkaUtil.sh status</li>
                    <li>sudo utils/kafkaUtil.sh stop</li>
                </ol>
                <li><b>Stop ElasticSearch – all 3 nodes.</b></li>
                <ol>
                    <li>sudo service elasticsearch stop</li>
                    <li>ps -ef | grep elastic</li>
                </ol>
                <li><b>Stop Logstash</b></li>
                <ol>
                    <li>sudo service logstash stop</li>
                </ol>
                <li><b>Stop Kibana : Get the pid for port 5601 using ‘netstat’ command and kill the process.</b></li>
                <ol>
                    <li>ps -ef | grep kibana</li>
                    <li>sudo kill -9 [process_id]</li>
                    <li>sudo netstat -nlp | grep :5601</li>
                </ol>
	    	</ul>
            </br></br>
            <p><b>Start Services</b></p>
            <ul>
                <li><b>Start ElasticSearch – all 3 nodes.</b></li>
                <ol>
                    <li>sudo service elasticsearch start</li>
                    <li>ps -ef | grep elastic</li>
                    <li>curl http://localhost:9200</li>
                </ol>
                <li><b>Start Logstash</b></li>
                <ol>
                    <li>sudo service logstash start</li>
                </ol>
                <li><b>Start Kibana</b></li>
                <ol>
                    <li>sudo /apps/kibana/latest/bin/kibana &</li>
                    <li>ps -ef | grep kibana</li>
                    <li>curl http://localhost:5601</li>
                    <li>sudo netstat -nlp | grep :5601</li>
                </ol>
                <li><b>Start Kafka/ZooKeeper – all 3 nodes.</b></li>
                <ol>
                    <li>sudo utils/kafkaUtil.sh start</li>
                </ol>
                <li><b>Start Kafka Connect – all 3 nodes.</b></li>
                <ol>
                    <li>sudo utils/connectUtil.sh status</li>
                    <li>sudo utils/connectUtil.sh start</li>
                    <li>sudo netstat -nlp | grep :8083</li>
                    <li>curl -XGET 'localhost:8083/connectors' | jq</li>
                    <li>curl -XGET 'localhost:8083/connectors/epq_wmxd_jdbc/status' | jq</li>
                    <li>curl -XGET 'localhost:8083/connectors/epq_omxd_jdbc/status' | jq</li>
                </ol>
                <li><b>Resume/Restart OM/WM listeners.</b></li>
                <li><b>Start Spark Cluster.</b></li>
                <ol>
                    <li>sudo su -l %s</li>
                    <li><b><mark>[%s] /apps/spark/latest/sbin/start-all.sh</mark></b></li>
                    <li>[others] /apps/spark-2.2.0-bin-hadoop2.7/sbin/start-all.sh</li>
                </ol>
                <li><b>Start Spark custom job</b></li>
                <ol>
                    <li>sudo su -l %s</li>
                    <li><b><mark>[%s] ./utils/sparkSubmitWMx.sh start, ./utils/sparkSubmitOMx.sh start</li></b>
                    <li>[others] ./utils/sparkSubmit.sh start</li>
                    <li>http://[target_primary_data_node_host]:8080/</li>
                </ol>
	    	</ul>
        </body>
    </html>
    """ % (host, os.getenv("SPARK_USER"), os.getenv("SPARK_UPGRADE"), os.getenv("SPARK_USER"), os.getenv("SPARK_UPGRADE"), os.getenv("SPARK_USER"), os.getenv("SPARK_CUSTOM_APPS"))


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), item_id: str = Form(...), description: str = Form(...)):
    try:
        file_location = f"{directory}/uploads/{file.filename}"
        logger.info(f"file_location : {file_location}")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "info": f"file '{file.filename}' saved at '{file_location}'",
            "item_id": item_id,
            "description": description
        }
    except Exception as e:
        logger.error(e)


@app.get("/filelist",
          status_code=200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:7091/filelist", 
          summary="* Return filelist in the form of JSON"
        )
async def get_download_file_list():
    current_directory = "{}/uploads".format(directory)
    logger.info(f"current dir : {current_directory}")
    dir_list = os.listdir(current_directory)

    ''' return fil list as type of list'''
    return dir_list
    

@app.get("/download/{filename}",
          status_code=200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:7091/download/<file_name>", 
          summary="* Return file"
         )
async def download_file(filename: str):
    try:
        # current_directory = os.getcwd()
        current_directory = directory
        file_path = os.path.join(current_directory, "uploads", filename)
        logger.info(f"file path : {file_path}")
        if not os.path.exists("{}".format(file_path)):
            return JSONResponse(status_code=404, content={"message": f"{filename} is not found"})
        return FileResponse(path=file_path, filename=filename)
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})