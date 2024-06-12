'''config variables'''
#if you want to temporary change on of these values
#copy it into the next line and place a # infront of the old line

#path to folder where the images should be stored
IMG_PATH = r''

#path to folder where the tags should be stored
TAGS_PATH = IMG_PATH

#format in which tags should be saved:
#none: No tags are saved
#text: as a txt-file; one line per image
#json: as a json-file; {id:[tags]}
#meta: as a json-file + save some additional info (see below)
#hydrus: as a folder of txt-files (one per image)
TAGS_FORMAT = 'none'

#True / False; Quick is ~2 times faster when getting images
# and ~20 times faster for tags but can't get child-posts nor all meta info
QUICK = True

#ONLY FOR DOWNLOADER
#tags; just like the seachbar on the booru
TAGS = ''

#ONLY FOR FAVORITES
#id of user; can be found in url when viewing users favorites
USER_ID = 0

#you could change the booru here but it might not work
URL = 'https://censored.booru.org/index.php'

#meta-info:
#normal: tags, rating, score, user, posted, source, parent
#quick : tags, rating, score, user

import os
def verify():
    '''verify if the values of all variables are okay'''
    if TAGS_FORMAT not in ('none', 'text', 'json', 'meta', 'hydrus'):
        raise ValueError(f'TAGS must be none|text|json|meta|hydrus not {TAGS}')
    if QUICK not in (True, False):
        raise ValueError(f'QUICK must be True or False but is {QUICK}')
    if QUICK and TAGS_FORMAT == 'meta':
        print('WARNING not all meta-info can be obtained when QUICK = True')
    if not os.path.exists(IMG_PATH):
        print(f'IMG_PATH ({IMG_PATH}) doesn\'t exist. It will now be created')
        try:
            os.makedirs(IMG_PATH, exist_ok=True)
        except OSError as os_e:
            raise ValueError(f'IMG_PATH ({IMG_PATH}) isn\'t a valid path') from os_e
    _path = TAGS_PATH + '\\_tags'*(TAGS_FORMAT=='hydrus')
    if not os.path.exists(_path):
        print(f'TAGS_PATH ({_path}) doesn\'t exist. It will now be created')
        try:
            os.makedirs(_path, exist_ok=True)
        except OSError as os_e:
            raise ValueError(f'TAGS_PATH ({_path}) isn\'t a valid path') from os_e
