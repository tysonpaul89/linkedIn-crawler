""" Main file """
import os
import pickle
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from config import timeout, dir_path, crawl_urls, credentials, cookie_file, screenshot_dir,\
    db

db.purge()

# Gets chrome driver path
chrome_driver_path = os.path.join(dir_path, 'chromedriver')

# To open browser on incognito(private) mode
browser_options = webdriver.ChromeOptions()
browser_options.add_argument('--incognito')
# browser_options.add_argument("--headless")

# Creates new instance of chrome
browser = webdriver.Chrome(
    executable_path=chrome_driver_path,
    chrome_options=browser_options
)

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
        pickle.dump(browser.get_cookies() , open(cookie_file,"wb"))

        # Taking screenshot
        browser.save_screenshot(screenshot_dir + 'homepage_from_auth.png')
    else: # restore session from cookie
        print('--- From cookie ---')
        browser.get(crawl_urls['home'])

        # Loads the cookies and refresh the page
        cookies = pickle.load(open(cookie_file, "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)

        browser.refresh()

        # Wait till the element is located
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'core-rail'))
        )
        # Taking screenshot
        browser.save_screenshot(screenshot_dir + 'homepage_from_cookie.png')

    # search link
    search_link = 'https://www.linkedin.com/search/results/people/?keywords='
    # search keywords
    search_keywords = ['hr', 'hiring', 'acquisition']

    # Search
    s_link = search_link + search_keywords[0]
    browser.get(s_link)
    # Wait till the element is located
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'search-results__list'))
    )

    # Scroll top bottom
    # Ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Get All search result items
    search_results = browser.find_elements_by_class_name('search-result__info')

    search_data = []
    for result in search_results:
        link = result.find_element_by_class_name('search-result__result-link')\
                .get_attribute('href').strip()
        id = link.split('-')[-1].replace('/', '')
        search_data.append({
            'id': id,
            'link': link,
            'name': result.find_element_by_class_name('actor-name').text.strip(),
            'occupation': result.find_element_by_class_name('subline-level-1').text.strip(),
            'location': result.find_element_by_class_name('subline-level-2').text.strip()
        })

    db.insert_multiple(search_data)

    'artdeco-pagination__button--next'

    """" Commented code for later purposes
    # Click on the my network link
    network_li_element = browser.find_element_by_id('mynetwork-nav-item')
    network_li_element.click()

    # Wait till the element is located
    WebDriverWait(browser, timeout).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'pymk-card'))
    )

    # Get All li elements from 'People You May Know' list
    pymk_cards = browser.find_elements_by_class_name('pymk-card')

    # WIP: Loop pymk_li and extract profile link, image, name and title
    user_data = []
    for card in pymk_cards:
        link = card.find_element_by_class_name('pymk-card__link').get_attribute('href')
        id = link.split('-')[-1].replace('/', '')
        user_data.append({
            'id': id,
            'name': card.find_element_by_class_name('pymk-card__name').text,
            'job' : card.find_element_by_class_name('pymk-card__occupation').text,
            'link': link
        })

    db.insert_multiple(user_data)"""

except TimeoutException:
    print('Timed out waiting for page to load')
    # Taking screenshot
    browser.save_screenshot(screenshot_dir + 'timeout_exception.png')
    browser.quit()



print('ok')