'''get all favorited images (and their tags)'''
import download

download.PARAMS = {
    'page': 'favorites',
    's': 'view',
    'id': download.config.USER_ID
}
download._page_size = 50
download._get_script = lambda span: span.next_sibling

if __name__ == '__main__':
    try:
        if not download.config.QUICK:
            raise ValueError('QUICK needs to be True for favorites')
        download.main()
    except Exception as e:
        print(f'Error: {e}')
        input('Press Enter to close')
