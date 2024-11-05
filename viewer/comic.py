import os
from pathlib import Path
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

app.mount("/static", StaticFiles(directory="./viewer/static"), name="static")
app.mount("/viewer/comic", StaticFiles(directory="./viewer/comic"), name="comic")

env = Environment(loader=FileSystemLoader('./viewer/templates'))
comic_env = Environment(loader=FileSystemLoader('./viewer/comic'))

@app.get('/', response_class=HTMLResponse)
async def index(req: Request):
    page = env.get_template('index.html')
    comic_folder_list = list(Path('./viewer/comic').glob('*'))
    return page.render(comic_list=''.join([p.stem for p in comic_folder_list]))

@app.get('/{comic_name}', response_class=HTMLResponse)
async def index(req: Request, comic_name: str):
    page = comic_env.get_template(f'{comic_name}/{comic_name}.html')
    comic_folder_list = list(Path('./viewer/comic').glob('*'))
    return page.render(comic_list=''.join([p.stem for p in comic_folder_list]))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('viewer.comic:app',
                host='localhost',
                port=4000,
                reload=True,
                log_level='debug')
