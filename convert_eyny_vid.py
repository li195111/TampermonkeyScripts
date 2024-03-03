import os
import shutil
import subprocess as sp
from pathlib import Path
from typing import List

from dotenv import load_dotenv

from models.logger import logger


if __name__ == '__main__':
    load_dotenv()
    file_path = Path(__file__)
    os.environ['LOG_DIR'] = file_path.parent.joinpath('logs').as_posix()
    log = logger(name=file_path.name,
                 level=10 if os.getenv("DEBUG") else 20)

    dst_dirs = [
        Path(os.getenv('EYNY_DOWNLOAD_DST_PATH')),
        Path(os.getenv('OLD_EYNY_DOWNLOAD_DST_PATH')),
    ]
    finished_vids: List[Path] = []
    for dst_dir in dst_dirs:
        if dst_dir.exists():
            finished_vids.extend(list(dst_dir.rglob('*.cache')))
    log.info('Total: %s', len(finished_vids))

    for cache_path in finished_vids:
        base_name = cache_path.stem
        dir_path = cache_path.parent
        vid_path = dir_path.joinpath(base_name)
        mkv_path = dir_path.joinpath(base_name.replace('mp4', 'mkv'))
        # logger.info('Process: %s', dir_path.stem)
        if vid_path.exists() and not mkv_path.exists():
            cmd = f'avidemux_cli.exe --load "{vid_path}" --output-format MKV --save "{mkv_path}"'
            out = sp.check_output(cmd,
                                  shell=True,
                                  cwd=os.getenv('AVIDEMUX_CLI_PATH'),
                                  stderr=sp.STDOUT)
            try:
                is_error = ('Error' in out.decode())
            except UnicodeDecodeError:
                is_error = ('Error' in out)
            if is_error:
                log.warning('Remove Error File: %s', dir_path)
                shutil.rmtree(dir_path.as_posix())
        else:
            ...
    # logger.info('Finished: %s', dir_path.stem)
