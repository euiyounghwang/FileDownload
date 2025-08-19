
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
import random
import string
import secrets
from passlib.context import CryptContext

'''
In Python, cryptographic hashing is primarily handled by the hashlib module for general-purpose hashing and 
the crypt module (though deprecated) or external libraries like bcrypt and passlib for password hashing.
'''
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



host = os.getenv("HOST")
# directory = r'C://Users/euiyoung.hwang/Git_Workspace/FileDownload'
directory = os.getenv("FILE_DIR")

if not os.path.isdir(directory + "/docs"):                                                           
    os.mkdir(directory + "/docs")

if not os.path.isdir(directory + "/uploads"):                                                           
    os.mkdir(directory + "/uploads")

app = APIRouter(
    prefix="/elk",
)


@app.get("/generate_sg_password", 
          status_code=200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/elk/generate_sg_password?plain_text_password=test", 
          summary="Cluster Info")
async def generate_sg_password():
    ''' encrypt'''
    try:
        logger.info(f"generate_sg_password called")
        
        # length = random.randint(8, 16)
        length = 12
        """
        # characters = string.ascii_letters + string.digits + string.punctuation
        # characters = string.ascii_letters + string.digits + '@'
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        # characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + '@'
        password = ''.join(random.choice(characters) for i in range(length))
        """
        symbols = ['*', '%', '@', '#', '!', '$'] # Can add more

        ''' subtract for ascii_uppercase, digits and symbols'''
        length -= 3
        password = ""
        for _ in range(length):
            password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        password += secrets.choice(symbols)
        print(password)
     
        return {
            "generated_Password_len" : len(password),
            "generated_Password" : password,
            "bcrypted_Hash_generated_Password" : pwd_context.hash(password)
        }
    
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    

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



@app.get("/docs", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <head>
            <title>ELk Upgrade Docs</title>
            <style type='text/css'>
                p { font-size: 19px;}
                li {
                    font-size: 18px; line-height: 2em;
                }
            </style>
            <link rel="shortcut icon" href="http://%s:7091/static/image/favicon.ico" type="image/x-icon">

        </head>
        <body>
            <h1>The ES Team Service - Download documentation files for upgrading Elasticsearch v.8.17.0 with search guard as x-pack/Logstash/Kibana</h1>
            <li><b>Download documentation files for upgrading ELK Stack</b></li>
            <ol>
				<li><a href="http://%s:7091/elk/document/ELK_Upgrade_ES_V8_Monitoring_Setup.docx">Setup ELK_Upgrade Docs</a></li>
                <li><a href="http://%s:7091/elk/document/ELK_Upgrade_Kibana_Query">Setup Kibana Query Docs</a></li>
			</ol>
            <li><b>Search-Guard as x-pack url</b></li>
            <ol>
				<li><a href="https://docs.search-guard.com/latest/search-guard-versions">Search Guard FLx Version</a></li>
                <li><a href="https://subin-0320.tistory.com/174">Generate certs for the ssl certification (Korean)</a></li>
			</ol>
            <li><b>Util</b></li>
            <ol>
				<li><a href="https://bcrypt-generator.com/#google_vignette">Bcrypt Hash Generator</a></li>
			</ol>
        </body>
    </html>
    """ % (host, host, host)


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
            We need to pass the path to the CA root certificate which was used to sign the server certificate offered by that Elasticsearch node. This way, the client will be able to trust the server connection.
            </p>
            <p>
            The csr mode generates certificate signing requests (CSRs) that You can send to a trusted certificate authority to obtain signed certificates. The signed certificates must be in PEM format to work with Elasticsearch security features.
            </p>
            <BR />
            <!--<img src='http://%s:7091/static/image/csr_command.PNG' width="800" height="320" />-->
            <li><b>How to Get CA Signed Certificate from CSR File</b> (<a href='https://tutorialspedia.com/csr-certificate-signing-request-how-to-get-ca-signed-certificate-from-csr-file/'>LINK</a>, <a href='https://cornswrold.tistory.com/435'>LINK#2</a>, <a href='https://velog.io/@gweowe/OpenSSL-자체-인증서SELF-SIGNED-CERTIFICATE-만들기-MacOS'>LINK#3</a>, <a href='https://a-gyuuuu.tistory.com/356'>LINK#4</a>)</li>
            <ol>
				<li> In order to get a CA signed certificate for a domain, you first need to generate a CSR (Certificate Signing Request) and then follow additional steps to get it certified/signed by a Certificate Authority (CA) to make it a valid CA Signed Digital SSL Certificate</li>
			</ol>
            <li><b>Steps to Get a CA Signed Certificate from CSR File : to obtain a certificate from the CA (Certificate Authority), you must generate a CSR (Certificate Signing Request)</b></li>
            <ol>
				<li>Generate CSR Certificate Signing Request File (.csr) :  if you want to generate CSR File using OpenSSL, first run the below command to create a key file:</li>
                <li><b>openssl genrsa -out demo.com.key 2048</b></li>
                <li>The above command will generate a key file demo.com.key which we will use in the below command to generate CSR File demo.csr</li>
                <li><b>openssl req -new -key demo.com.key -out demo.csr</b></li>
                <li>Once you will run the above command for generating certificate signing request (CSR), you will be promoted to enter additional details including country, state, city, organization, organization unit, CN (common name), email etc.</li>
			</ol>
            <li><b>Submit CSR Certificate Signing Request File to CA to get Signed SSL Certificate</b></li>
            <ol>
				<li>Once you have created a CSR File using step 1, next you need to submit the CSR to a CA</li>
                <li>Create Self Signed Certifcate : `openssl x509 -req -days 365 -in ca.csr -signkey ca.key -out ca.crt` or `openssl x509 -req -days 365 -extensions v3_ca -set_serial -in ca.csr -signkey ca.key -out ca.crt -extfile csr_file.conf`</li>
                <li><b>The CA will then validate the information in the CSR, and if everything is in order, they will issue a signed certificate</b></li>
                <li>When submitting the CSR to the CA, you will typically be prompted to provide additional information such as your organization’s contact details and the domain name(s) that the certificate will be used for. The CA will use this information to validate your organization and ensure that you are authorized to request a certificate for the domain in question.</li>
			</ol>
            <li><b>Install CA Signed SSL Certificate on Server</b></li>
            <ol>
				<li>Once you have received the signed certificate, you will need to install it on the server along with the private key that was generated when the CSR was created</li>
                <li><b>After the certificate is installed, it can be used for SSL Based secure communications such as HTTPS.</b></li>
			</ol>
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
				<li><a href="http://%s:7091/elk/download/qa13-es8-ca.pem">QA-13 CA certificate (PEM format)</a>, <a href="http://%s:7091/elk/download/qa13-es-certs.jks">QA-13 CA certificate (jks format)</a>, <a href="http://%s:7091/elk/download/qa13-es-certs.p12">QA-13 CA certificate (p12 format)</a></li>
			</ol>
            <li><b>PROD Environment</b></li>
	    	</ul>
        </body>
    </html>
    """ % (host, host, host, host)


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
    

@app.get("/document/{filename}",
          status_code=200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:7091/document/<file_name>", 
          summary="* Return file"
         )
async def download_file(filename: str):
    try:
        # current_directory = os.getcwd()
        current_directory = directory
        file_path = os.path.join(current_directory, "docs", filename)
        logger.info(f"file path : {file_path}")
        if not os.path.exists("{}".format(file_path)):
            return JSONResponse(status_code=404, content={"message": f"{filename} is not found"})
        return FileResponse(path=file_path, filename=filename)
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})