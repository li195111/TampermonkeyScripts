import os
import glob
import cv2
import numpy as np


proj_path = 'F:/Study/妹妹的義務'

proj_name = os.path.basename(proj_path)

search_regex = f'{proj_path}/*/*.jpg'
ver_names = os.listdir(proj_path)
# img_paths = glob.glob(search_regex, recursive=True)
n_vers = len(ver_names)

viewH = 800
step = 20
wait = 5
ver_i = 0
im_i = 0
prv_img_path = None
prv_img = None

nxt_img_path = None
nxt_img = None
window_name = f'{proj_name}'
while ver_i < len(ver_names):
  ver_name = ver_names[ver_i]
  ver = ver_name.split('_')[0]
  ver_path = os.path.join(proj_path, ver_name)

  ver_img_names = os.listdir(ver_path)
  n_imgs = len(ver_img_names)
  ver_img_paths = [os.path.join(ver_path,im_name) for im_name in ver_img_names]
  
  if im_i == n_imgs:
    im_i = 0
    ver_i += 1
    ver_i = min(ver_i,n_vers-1)
  elif im_i < 0:
    ver_i -= 1
    ver_i = max(ver_i,0)
  else:
    cur_img_path = ver_img_paths[im_i]

    if im_i > 0:
      prv_img_path = ver_img_paths[im_i-1]
    if im_i < n_imgs-1:
      nxt_img_path = ver_img_paths[im_i+1]
      
    img = cv2.imread(cur_img_path)
    imH, imW = img.shape[:2]
    
    if not prv_img_path is None:
      prv_img = cv2.imread(nxt_img_path)
      prvH, prvW = prv_img.shape[:2]
      prv_img = cv2.resize(prv_img, (imW, prvH), interpolation=cv2.INTER_LANCZOS4)

    if not nxt_img_path is None:
      nxt_img = cv2.imread(nxt_img_path)
      nxtH, nxtW = nxt_img.shape[:2]
      img = cv2.resize(img, (nxtW, imH), interpolation=cv2.INTER_LANCZOS4)
    imH, imW = img.shape[:2]

    i = 0
    while i < (imH - viewH):
      if i < 0:
        prvious_img = prv_img[i:].copy()
        show = img[:i+viewH].copy()
      else: 
        prvious_img = np.empty((0,imW,3),np.uint8)
        show = img[i:i+viewH].copy()
      retain_H = viewH - show.shape[0]
      retain_img = nxt_img[:retain_H].copy()
      show = np.concatenate([prvious_img,show,retain_img],0)

      cv2.putText(show, f'{ver}', (20,40), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
      cv2.imshow(window_name, show)
      key = cv2.waitKey(wait)
      if key == 27 or key == ord('q'):
        break
      elif key == ord('s'):
        wait += 1
        wait = min(wait,500)
      elif key == ord('f'):
        wait -= 1
        wait = max(wait,0)
      elif key == ord('n'):
        break
      elif key == ord('N'):
        break
      elif key == ord('v'):
        break
      elif key == ord('V'):
        break
      elif key == ord('t'):
        if wait:
          wait = 0
        else:
          wait = 5
      elif key == ord('p'):
        i -= step
      else:
        i += step
    if key == 27 or key == ord('q'):
      break
    elif key == ord('n'):
      im_i += 1
    elif key == ord('N'):
      im_i -= 1
    else:
      im_i += 1
    if key == ord('v'):
      ver_i += 1
      ver_i = min(ver_i,n_vers-1)
      im_i = 0
    elif key == ord('V'):
      ver_i -= 1
      ver_i = max(ver_i,0)
      im_i = 0
cv2.destroyAllWindows()