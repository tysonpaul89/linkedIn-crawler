""" Main file """
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import timeout, dir_path, crawl_urls, credentials, cookie_name

# Gets chrome driver path
chrome_driver_path = os.path.join(dir_path, 'chromedriver')

# To open browser on incognito(private) mode
browser_options = webdriver.ChromeOptions()
browser_options.add_argument('--incognito')

# Creates new instance of chrome
browser = webdriver.Chrome(
    executable_path=chrome_driver_path,
    chrome_options=browser_options
)

# Gets cookie file name
cookie_file = os.path.join(dir_path, cookie_name)

try:
    # Login if cookie is not present
    if (not os.path.isfile(cookie_file)):
        print('--- Login ---')
        # Requests login page
        browser.get(crawl_urls['login'])

        # Wait till the element is present on the DOM
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.ID, 'login-submit'))
        )

        # Does Authentication by filling form email and password and clicking on login button
        browser.find_element_by_id('login-email').send_keys(credentials['email'])
        browser.find_element_by_id('login-password').send_keys(credentials['password'])
        browser.find_element_by_id('login-submit').click()

        # Wait till the 'core-rail' class is located
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'core-rail'))
        )

        # Saves the cookies
        pickle.dump(browser.get_cookies() , open(cookie_name,"wb"))
    else: # restore session from cookie
        print('--- From cookie ---')
        browser.get(crawl_urls['home'])

        # Loads the cookies and refresh the page
        cookies = pickle.load(open(cookie_name, "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)

        browser.refresh()

        # Wait till the element is located
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'core-rail'))
        )

        # Click on the my network link
        browser.find_element_by_xpath('//*[@id="mynetwork-nav-item"]/a').click()

        # Wait till the element is located
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'left-rail'))
        )
except expression as identifier:
    print('Timed out waiting for page to load')
    browser.quit()



print('ok')