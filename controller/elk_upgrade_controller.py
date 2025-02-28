
from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
# from controller import db_controller
from config.log_config import create_log
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
          description="Sample Payload : http://localhost:8001/cluster/health?es_url=http://localhost:9200", 
          summary="Cluster Info")
async def get_es_health(plain_text_password="test"):
    ''' encrypt'''
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



@app.get("/ca_file", response_class=HTMLResponse)
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


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), item_id: str = Form(...), description: str = Form(...)):
    try:
        file_location = f"{directory}/uploads/{file.filename}"
        print(f"file_location : {file_location}")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "info": f"file '{file.filename}' saved at '{file_location}'",
            "item_id": item_id,
            "description": description
        }
    except Exception as e:
        print(e)


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
        print(f"file path : {file_path}")
        if not os.path.exists("{}".format(file_path)):
            return JSONResponse(status_code=404, content={"message": f"{filename} is not found"})
        return FileResponse(path=file_path, filename=filename)
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": str(e)})