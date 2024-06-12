'''download images, tags and meta-info'''
import os
import re
from time import sleep
import requests as r
import bs4 as _bs4
from bs4 import BeautifulSoup as bs4

import config
import tags

PARAMS = {
    'page': 'post',
    's': 'list',
    'tags': config.TAGS or 'all'
}
_page_size = 20
_get_script = lambda span: span.select_one('script')

def main():
    '''load config; download imgs (+tags); save tags'''
    config.verify()
    soup = bs4(r.get(config.URL, params=PARAMS, timeout=5).text, 'lxml')
    if config.QUICK:
        last_pid = int(soup.select_one('a[alt="last page"]').attrs['href'].split('pid=')[-1])
        for _pid in range(0, last_pid+1, _page_size):
            print(f'Getting {_pid = }')
            get_posts(_pid)
    else:
        last_id = int(soup.select_one('span.thumb>a:has(img)').attrs['href'].split('id=')[-1])
        PARAMS['s'] = 'view'
        for _id in range(0, last_id+1):
            if _id % 10 == 0:
                print(f'Getting {_id = }')
            get_post(str(_id))

    tags.save_tags(tags.DATA)

def get_posts(pid:int):
    '''get all post of the list page'''
    try:
        p = r.get(config.URL, params=PARAMS|{'pid': pid}, timeout=5)
        if p.status_code != 200:
            print('Waiting for Censoredbooru...')
            sleep(3)
            p = r.get(config.URL, params=PARAMS|{'pid': pid}, timeout=5)
        soup = bs4(p.text, 'lxml')
        for post in soup.select('span.thumb'):
            parse_post(post)
    except Exception as e1:
        print(f'Error in get_posts(pid={pid}):', e1)

def parse_post(post:_bs4.element.Tag):
    '''parse a post from the list page'''
    img_id = post.select_one('a').attrs['id'][1:]
    try:
        tags.DATA[img_id] = tags.get_tags_quick(_get_script(post))

        img_set, img_hash, img_end = re.findall(
            r'\/(\d+)\/thumbnail_([0-9a-f]+)\.(png|jpeg|jpg|gif)',
            post.select_one('a > img').attrs['src'], re.IGNORECASE
        )[0]

        img_path = os.path.join(config.IMG_PATH, f'{img_id}.{img_end}')
        img_url = f'https://img.booru.org/censored//images/{img_set}/{img_hash}.{img_end}'

        save_image(img_path, img_url)
    except Exception as e1:
        print(f'Error in parse_post(id={img_id}):', e1)

def get_post(img_id:str|int):
    '''get and parse a post from the view page'''
    try:
        p = r.get(config.URL, params=PARAMS|{'id': img_id}, timeout=5)
        if p.status_code != 200:
            print('Waiting for Censoredbooru...')
            sleep(5)
            p = r.get(config.URL, params=PARAMS|{'id': img_id}, timeout=5)
        if p.url != config.URL+'?page=post&s=list':
            return
        soup = bs4(p.text, 'lxml')

        tags.DATA[img_id] = tags.get_tags(soup)

        img_url = soup.select_one("img").attrs['src']
        img_end = img_url.split('.')[-1]
        img_path = os.path.join(config.IMG_PATH, f'{img_id}.{img_end}')

        save_image(img_path, img_url)
    except Exception as e1:
        input((f"Error in get_post({img_id = })", e1))

def save_image(img_path, img_url):
    '''save an image'''
    if not os.path.exists(img_path):
        with open(img_path, 'wb') as file:
            file.write(r.get(img_url, timeout=30).content)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
        input('Press Enter to close')
