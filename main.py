import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, StreamingResponse

from lib.file import File
from lib.db import DB
from lib.ftp import UploadFtp

app = FastAPI()
templates = Jinja2Templates(directory="./static/templates")
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

with open("./conf/conf.json", "r") as f:
    config = json.loads(f.read())


@app.get("/")
async def read_root(request: Request):
    all_files = DB.get_files(config["db"])
    dict_files = [file.__dict__ for file in all_files]

    return templates.TemplateResponse("index.html", {"request": request, "files": dict_files})


@app.get("/file/{file_id}")
async def read_file(request: Request, file_id: int):
    file = DB.get_file(config["db"], file_id)

    if file is None:
        return Response(status_code=404)

    return templates.TemplateResponse("file.html", {"request": request, "file": file.__dict__})


@app.get("/file/{file_id}/download")
async def download_file(request: Request, file_id: int):
    file = DB.get_file(config["db"], file_id)

    if file is None:
        return Response(status_code=404)

    f = UploadFtp.download(config["ftp"], file.filename)
    f.seek(0)

    return StreamingResponse(f)


@app.post("/upload")
async def upload(request: Request):
    file = File("form_data", await request.form())
    await file._calc_size()
    await file.save(config["db"], config["ftp"])

    return {"message": "File uploaded successfully"}
