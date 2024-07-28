import glob
import os
import shutil

from utils import FileSizeLevel, count_bytes_level

if __name__ == '__main__':
  docs_dir = 'C:/Users/a0983/Downloads/'
  download_dir = 'D:/Study'
  vid_dir_regex = os.path.join(download_dir,
                               'eyny_*').replace('[',
                                                 '[[]').replace(']', '[]]')
  vid_dirs = glob.glob(vid_dir_regex, recursive=True)
  for dir_idx, dir_path in enumerate(vid_dirs):
    dir_name = os.path.basename(dir_path)
    cache_regex = os.path.join(dir_path,
                               '*.cache.download').replace('[', '*').replace(
                                   ']', '*')
    cache_downloads = glob.glob(cache_regex, recursive=True)
    is_downloading = len(cache_downloads) > 0
    # print('Cache Files:', cache_regex, cache_downloads)

    media_regex = os.path.join(dir_path,
                               '*.mp4').replace('[', '*').replace(']', '*')
    media_paths = glob.glob(media_regex, recursive=True)
    has_media = len(media_paths) > 0
    media_sizes = [os.path.getsize(vid) for vid in media_paths]
    # print('Media Files:', vid_regex, vid_paths)

    doc_file_regex = os.path.join(dir_path, 'downloaded',
                                  '*.txt').replace('[', '*').replace(']', '*')
    doc_files = glob.glob(doc_file_regex, recursive=True)
    has_doc = len(doc_files) > 0

    ttl_bytes = 0
    total_numb = 0
    total_level = FileSizeLevel.KB
    print(
        f'{dir_idx:04d} Sizes: {str(media_sizes):13s} Downloading: {str(is_downloading):>5s}, Doc: {str(has_doc):>5s}, Media: {str(has_media):>5s}, Dir: {dir_name[:20]:25s}'
    )
    try:
      if len(media_paths) == 0 and len(doc_files) == 0:
        if len(cache_downloads) == 0:
          print(f'Remove empty: {dir_path}')
          # shutil.rmtree(dir_path)
      elif len(media_paths) > 0 and len(doc_files) == 0:
        if len(cache_downloads) == 0:
          print(f'Remove no download file: {dir_path}')
          # shutil.rmtree(dir_path)
      elif len(media_paths) == 0 and len(doc_files) > 0:
        doc_path = doc_files[0]
        doc_name = os.path.basename(doc_path)
        dst_path = os.path.join(docs_dir, doc_name)
        print(f'Move to queue: {doc_path} -> {dst_path}')
        # shutil.move(download_file, dst_path)
      else:
        # has download .txt file and .mp4 media file
        media_path = media_paths[0]
        ttl_bytes = os.path.getsize(media_path)
        total_numb, total_level = count_bytes_level(ttl_bytes)
        if total_level == FileSizeLevel.KB and ttl_bytes == 0:
          doc_path = doc_files[0]
          doc_name = os.path.basename(doc_path)
          dst_path = os.path.join(docs_dir, doc_name)
          print(f'Move to queue: {doc_path} -> {dst_path}')
          # shutil.move(download_file, dst_path)
          print(f'Remove no download file: {dir_path}')
          # shutil.rmtree(dir_path)
    except PermissionError:
      print(f'Pass - {dir_idx} Dir: {dir_name}')
