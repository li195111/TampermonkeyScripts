import glob
import os
import subprocess
import threading
from typing import List

if __name__ == '__main__':
  work_dir = os.path.dirname(__file__)
  out_dir = os.path.join(work_dir, 'Arch')
  os.makedirs(out_dir, exist_ok=True)
  module_paths = glob.glob(
      os.path.join(work_dir, '*', '__init__.py'))
  ts: List[threading.Thread] = []
  for module_path in module_paths:
    module_dir = os.path.dirname(module_path)
    module_name = os.path.basename(module_dir)
    cmd = f'pyreverse -o svg -p {module_name} -d {out_dir} {module_dir}'
    t = threading.Thread(target=subprocess.check_output, args=(cmd,))
    t.start()
    ts.append(t)

  for t in ts:
    t.join()
