#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
import random
from time import sleep

# web driver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from .constants import SCRIPTS
# ---------------------------------------------------------
# browser
# ---------------------------------------------------------
driver=None
old_height=0

def launchBrowser(Debug=False):
    '''
        Browser options
    '''
    
    global driver

    options = Options()
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.add_experimental_option('prefs', prefs)
    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    if not Debug:
        options.add_argument("--headless")
    
    
    try:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options) #--this is kept for local testing
        
    except Exception as e:
        print(e)
        exit(1)
    
    return driver


# ---------------------------------------------------------
def check(element,xpath):
    '''
        checks an element by xpath
    '''
    try:
        element.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False

def waitSomeTime(mult=None):
    '''
        Waits some seconds in between high and low
    '''
    _wait_time=round(random.random()*2 + 1,2)

    if mult is None:
        sleep(_wait_time)
    else:
        for _ in range(mult):
            sleep(_wait_time)

# ---------------------------------------------------------            
def scrollCheckHeight():
    '''
    check if height changed

    '''
    global old_height
    new_height = driver.execute_script(SCRIPTS.scrollHeight)
    return new_height != old_height


def scroll():
    '''
        helper function: used to scroll the page
    '''
    global old_height
    try:
        old_height = driver.execute_script(SCRIPTS.scrollHeight)
        # scroll 
        driver.execute_script(SCRIPTS.scroll)
        # wait
        WebDriverWait(driver, 10, 0.05).until(lambda x: scrollCheckHeight())

    except Exception as e:
        print(e)
# ---------------------------------------------------------            

def clickLink(link):
    '''
        clicks a link
    '''
    
    try:
        # click
        link.click()    
    except Exception as e1:
        try:
            driver.execute_script(SCRIPTS.click,link)
        except Exception as e2:
            pass

            
