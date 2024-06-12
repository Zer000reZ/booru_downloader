'''handle getting and saving the tags (and meta-info)
format: {<id>:{'tags':[<tags>], <meta as k,v pair>}}'''
import os
import re
import json
import html

import config

#booru-hash = sha1(md5(raw-img).hexdigest().encode())

DATA = {}

def save_tags(data:dict):
    '''save the tags'''
    if config.TAGS_FORMAT == 'none':
        return

    if config.TAGS_FORMAT == 'hydrus':
        for i in data:
            fp = os.path.join(config.TAGS_PATH, f'_tags\\{i}.txt')
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(' '.join(data[i]['tags']))
        return

    if config.TAGS_FORMAT == 'text':
        fp = os.path.join(config.TAGS_PATH, '_tags.txt')
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                old = {
                    line.split(': ',1)[0] : line.split(': ',1)[1].split(' ')
                    for line in f.read().split('\n')
                }
        else:
            old = {}
        old.update({k: v['tags'] for k,v in data.items()})
        with open(fp, 'w', encoding='utf-8') as f:
            f.write('\n'.join(f'{k}: {" ".join(v)}'
                for k,v in sorted(old.items(), key=lambda x:int(x[0]))))
        return

    if config.TAGS_FORMAT == 'json':
        fp = os.path.join(config.TAGS_PATH, '_tags.json')
        data = {k: v['tags'] for k,v in data.items()}
    if config.TAGS_FORMAT == 'meta':
        fp = os.path.join(config.TAGS_PATH, '_tags_meta.json')

    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            old = json.load(f)
    else:
        old = {}
    old.update(data)
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(old, f)
    return

def get_tags(soup) -> dict[str, str|list|int]:
    '''get tags (+meta) given the soup'''
    stats = ''.join(i for i in soup.select_one("#tag_list>ul").children if i.name is None)

    cdata = {
        'tags': parse_tags(soup.select_one("#tags").text),
        'posted': re.findall('Posted: (.*)', stats)[0].strip(),
        'user': re.findall('By: (.*)', stats)[0].strip(),
        'source': re.findall('Source: (.*)', stats)[0].strip(),
        'rating': re.findall('Rating: (.*)', stats)[0].strip(),
        'score': int(re.findall('Score: (.*)', stats)[0].strip())
    }

    parent = soup.select_one('input[name="parent"]').attrs['value'].strip()
    if parent:
        cdata['parent'] = parent
    return cdata

def get_tags_quick(script) -> dict[str, str|list|int]:
    '''get tags (+meta) given the soup for QUICK==True'''
    script = script.text
    return {
        'tags': parse_tags(re.findall(r"'tags':'(.+)'.split\(\/ \/g\),", script, re.DOTALL)[0]),
        'user': re.findall("'user':'(.+)'}", script)[0],
        'rating': re.findall("'rating':'([^']+)',", script)[0],
        'score': int(re.findall(r"'score':(-?\d+),", script)[0])
    }

def parse_tags(s:str) -> list[str]:
    '''parse str of tags into list of tags'''
    return html.unescape(s.replace('%20', ' ')).replace('\n','').replace('\r','').split(' ')
