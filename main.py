from fastapi import FastAPI, UploadFile, File, Form
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
# from controller import db_controller
from config.log_config import create_log
from fastapi.responses import FileResponse, HTMLResponse
import shutil

import os

# directory = 'c/Users/euiyoung.hwang/Git_Workspace/FileDownload'
directory = r'C://Users/euiyoung.hwang/Git_Workspace/FileDownload'

os.makedirs("uploads", exist_ok=True)

logger = create_log()
app = FastAPI(
    title="FileDownload API Service",
    description="FileDownload API Service",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi


''' http://localhost:7091/docs '''

@app.get("/", tags=['API'],  
         status_code=200,
         description="Default GET API", 
         summary="Return Json")
async def root():
    return {"message": "This API allow us to download any files"}


@app.get("/ui", response_class=HTMLResponse)
async def get_upload_form():
    return """
    <html>
        <head>
            <title>FileDownload Service - Upload File</title>
        </head>
        <body>
            <h1>The ES Team Service - Upload File with Extra Fields</h1>
            <form action="/uploadfile/" method="post" enctype="multipart/form-data">
                <input type="file" name="file"><br>
                <input type="text" name="item_id" placeholder="Item ID"><br>
                <input type="text" name="description" placeholder="Description"><br>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), item_id: str = Form(...), description: str = Form(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "info": f"file '{file.filename}' saved at '{file_location}'",
        "item_id": item_id,
        "description": description
    }


@app.get("/filelist")
async def get_download_file_list():
    current_directory = "{}/uploads".format(directory)
    dir_list = os.listdir(current_directory)

    ''' return fil list as type of list'''
    return dir_list
    

@app.get("/download/{filename}")
async def download_file(filename: str):
    # current_directory = os.getcwd()
    current_directory = directory
    file_path = os.path.join(current_directory, "uploads", filename)
    # FileResponse를 사용하여 파일을 다운로드 합니다.
    return FileResponse(path=file_path, filename=filename)


'''
@app.get("/test", tags=['API'],  
         status_code=200,
         description="Default GET Param API", 
         summary="Return GET Param Json")
async def root_with_arg(id):
    logger.info('root_with_arg - {}'.format(id))
    return {"message": "Hello World [{}]".format(id)}


@app.get("/test/{id}", tags=['API'],  
         status_code=200,
         description="Default GET with Body API", 
         summary="Return GET with Body Json")
async def root_with_param(id):
    logger.info('root_with_arg - {}'.format(id))
    return {"message": "Hello World [{}]".format(id)}
'''

# router
# app.include_router(db_controller.app, tags=["DB API"], )
