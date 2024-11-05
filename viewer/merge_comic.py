import os
import shutil
from pathlib import Path
from typing import List

from PIL import Image
from jinja2 import Environment, FileSystemLoader


def webp_to_jpg(input_path, output_path):
    # 開啟 WebP 圖片
    image = Image.open(input_path)

    # 如果圖片有 alpha 通道（透明度），將其轉換為 RGB
    if image.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])
        image = background

    # 儲存為 JPG
    image.save(output_path, 'JPEG', quality=95)


if __name__ == '__main__':
    env = Environment(loader=FileSystemLoader('./viewer/templates'))
    html_template = env.get_template('comic.html')
    # 1. Get the list of comic files
    comic_folder_list = list(Path('./viewer/comic').glob('*'))
    for comic_folder in comic_folder_list:
        comic_page_list: List[Path] = []
        if not comic_folder.is_dir():
            continue
        comic_sub_folder_list = list(comic_folder.glob('*'))
        comic_sub_folder_list = [
            x for x in comic_sub_folder_list if x.is_dir() and not x.stem in [comic_folder.stem]]
        comic_sub_folder_list.sort(key=lambda x: int(x.stem.split('_')[0]))
        for sub_folder in comic_sub_folder_list:
            if not sub_folder.is_dir():
                continue
            for img_type in ['jpg', 'webp']:
                sub_page_list = list(sub_folder.glob(f'*.{img_type}'))
                for sub_page in sub_page_list:
                    if sub_page.suffix == '.webp':
                        # 2. Convert webp to jpg
                        webp_to_jpg(sub_page, sub_page.with_suffix('.jpg'))
                        os.remove(sub_page)
                        sub_page = sub_page.with_suffix('.jpg')
                    comic_page_list.append(sub_page)
                    merge_folder = comic_folder.joinpath(comic_folder.stem)
                    merge_folder.mkdir(parents=True, exist_ok=True)
                    comic_no = sub_folder.stem.split('_')[0]
                    dst_path = comic_folder.joinpath(comic_folder.stem, f'{comic_no}_{sub_page.name}')
                    if not dst_path.exists():
                        shutil.copy(sub_page, dst_path)
            
        # 3. Merge comic pages
        comic_html_map = {}
        for comic in comic_page_list:
            comic_no = comic.parent.stem.split('_')[0]
            comic_html_template = """<img src="{img_src}" alt="{img_alt}">""".format(
                img_src=comic.relative_to('.').as_posix(),
                img_alt=comic.stem
            )
            if comic_no in comic_html_map:
                comic_html_map[comic_no].append(comic_html_template)
            else:
                comic_html_map[comic_no] = [comic_html_template]

        comic_no_html_block_list = []
        comic_no_html_template = """<div class="comic_block" id="{comic_no}">{comic_pages}</div>"""
        for comic_no, comic_pages in comic_html_map.items():
            comic_no_html_block = comic_no_html_template.format(
                comic_no=comic_no,
                comic_pages=''.join(comic_pages)
            )
            comic_no_html_block_list.append(comic_no_html_block)

        comic_html = html_template.render(
            title=comic_folder.stem,
            comic_no_blocks=''.join(comic_no_html_block_list)
        )
        with open(comic_folder.joinpath(f'{comic_folder.stem}.html'), 'w') as f:
            f.write(comic_html)
