import os
from pathlib import Path

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    os.environ['MONGO_COLLECTION'] = 'AVB_VIDEOS'
    os.environ['MONGO_SYS_COLLECTION'] = 'AVB_SYS'

    user_profile_dir = Path(os.environ['USERPROFILE'])
    src_dirs = [user_profile_dir.joinpath('Downloads')]
    dst_dir = Path(os.getenv('EYNY_DOWNLOAD_DST_PATH'))
    dst_dir.mkdir(parents=True, exist_ok=True)
    for src_dir in src_dirs:
        if src_dir.exists():
            if isinstance(src_dir, Path):
                src_dir = src_dir.as_posix()
            download_files = list(Path(src_dir).glob('*.download'))
            for download_file in download_files:
                without_ext = download_file.stem
                without_ext_file = download_file.parent.joinpath(without_ext)
                print(f'{download_file} -> {without_ext_file}')
                os.rename(download_file, (without_ext_file))
