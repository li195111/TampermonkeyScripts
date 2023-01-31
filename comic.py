# main_page = 'https://18comic.org/album/188259/'

# download_page_1 = 'https://18comic.org/album_download/188259'
# download_url_1 = 'https://dlzip.18comic.org/download_zip/188259?md5=r6J8bdYow9bvN5TENTJSJw&expires=1667529640&aid=188259'

# download_page_2 = 'https://18comic.org/album_download/326117'
# download_url_2 = 'https://dlzip.18comic.org/download_zip/326117?md5=xS6V3cAZsjLvs4vz2Rf8ZA&expires=1667529684&aid=326117'

# download_page_3 = 'https://18comic.org/album_download/190168'
# download_url_3 = ''

# import requests
# import cv2
# import numpy as np

# res = requests.get('https://18comic.org/captcha/0.1', headers={'Referer':'https://18comic.org/album_download/190168',
#                                                          'Accept':'image/avif,image/webp,*/*',
#                                                          'Accept-Encoding':'gzip, deflate, br'})
# img_arr = np.asarray(bytearray(res.content),dtype=np.uint8)
# img = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)
# cv2.imshow('Captcha', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
import os
import glob
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def index(req: Request):
  ver_dir = 'static/*/*.jpg'
  img_paths = glob.glob(ver_dir, recursive=True)
  img_eles = [f'<div class="img-block"><img src="{path}"></div>' for path in img_paths]
  html = f"""
  <!DOCTYPE html>
    <html lang="zh-tw">

    <head>
      <meta charset="utf-8" />
      <title>Comic Viewer</title>
    </head>

    <body style="background-color: #FFFFFF;">
      <div class="pages">{''.join(img_eles)}</div>
    </body>
    <link rel="stylesheet" href="static/css/comic.css">
    </html>
  """
  return html


@app.get("/comic")
def read_item(q: Union[str, None] = None):
  imgs = os.listdir('F:/Study/妹妹的義務/25_219293')
  print(imgs)
  html = '''
  <!DOCTYPE html>
  <html lang="zh-tw">

  <head>
    <meta charset="utf-8" />
    <title>Comic Viewer</title>
  </head>

  <body style="background-color: #FFFFFF;">
    <script>
      
    </script>
  </body>
  '''
  return


if __name__ == "__main__":
  import uvicorn
  uvicorn.run('comic:app',
              host='localhost',
              port=3000,
              reload=True,
              log_level='debug')
