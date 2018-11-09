import os

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