""" Main file """
import os
import pickle
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from config import timeout, dir_path, crawl_urls, credentials, cookie_file, screenshot_dir,\
    db




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
    for card in pymk_cards:
        print('image: ', card.find_element_by_class_name('lazy-image').get_attribute('src'))
        print('link: ',card.find_element_by_class_name('pymk-card__link').get_attribute('href'))
        print('name: ',card.find_element_by_class_name('pymk-card__name').text)
        print('job: ',card.find_element_by_class_name('pymk-card__occupation').text)
        print('------------------------')

except TimeoutException:
    print('Timed out waiting for page to load')
    # Taking screenshot
    browser.save_screenshot(screenshot_dir + 'timeout_exception.png')
    browser.quit()



print('ok')