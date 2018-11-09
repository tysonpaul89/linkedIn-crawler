import os
from tinydb import TinyDB, Query

# Domain name to crawl
domain = 'https://www.linkedin.com/'

# Urls to crawl
crawl_urls = {
    'login': domain,
    'home': domain,
}

# User credentials
credentials = {
    'email': '',
    'password': ''
}

# Wait time
timeout = 20

# Gets current directory path
dir_path = os.getcwd()

# Cookie file name to store cookies
cookie_name = 'cookies.pkl'

# Gets cookie file name
cookie_file = os.path.join(dir_path, cookie_name)

# Gets screenshot saving directory path
screenshot_dir = os.path.join(dir_path, 'screenshots' + os.sep)

# TinyDB Config
db_path = os.path.join(dir_path, 'db' + os.sep, 'db.json')
db = TinyDB(db_path)

