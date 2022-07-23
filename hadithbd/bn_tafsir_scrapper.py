#------------------------------
# imports
#------------------------------
import pandas as pd
import os
from selenium import webdriver
from time import sleep
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
from time import sleep
from selenium.webdriver.chrome.options import Options
from tqdm.auto import tqdm
from multiprocessing import Process
#------------------------------
# helpers
#------------------------------
def create_dir(base,ext):
    _path=os.path.join(base,ext)
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path 

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

#------------------------------
# globals
#------------------------------
arabic_xpath=".//div[@class='col-sm text-right font-arabic my-2 h2 showArabic']"
audio_path=".//source[@type='audio/mpeg']"
next_xpath=".//span[@class='nav_button nav_next']"
zakaria_xpath=".//div[@class='col-sm text-justify showZakaria']"
bayan_xpath=".//div[@class='col-sm text-justify showBayan']"
header_xpath=".//p[@class='text-dark font-weight-bold h4']"
xlation_xpath=".//div[@class='col-sm alert alert-secondary my-2']"
xlsrc_xpath=".//span[@class='badge text-muted font-italic font-weight-light']"

FILES=[]
TEXTS=[]
TZ=[]
TB=[]
TR=[]

batch=10 # how many surah's to download at once

save_dir="/home/ansary/WORK/Research/hadithbd/"
log_txt ="/home/ansary/WORK/Research/hadithbd/log.txt"

#----------------------------
# windows
#----------------------------
#driver = webdriver.Chrome('C:\\Users\\Shabab\\chromedriver')

options = Options()
prefs = {'profile.default_content_setting_values': {'images': 2}}
options.add_experimental_option('prefs', prefs)
#  Code to disable notifications pop up of Chrome Browser
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--mute-audio")
options.add_argument("--headless")

#----------------------------
# main page saving function
#----------------------------
def save_data(driver,spath):
    '''
        saving a single page of a sura
    '''
    global FILES,TEXTS,TZ,TB,TR
    # page
    audio_elems=driver.find_elements(By.XPATH,audio_path)
    text_elems =driver.find_elements(By.XPATH,arabic_xpath)
    tz_elems   =driver.find_elements(By.XPATH,zakaria_xpath)
    tb_elems   =driver.find_elements(By.XPATH,bayan_xpath)
    xl_elems   =driver.find_elements(By.XPATH,xlation_xpath)
    
    for txt_elem,audio_elem,tz_elem,tb_elem,xl_elem in zip(text_elems,
                                                            audio_elems,
                                                            tz_elems,
                                                            tb_elems,
                                                            xl_elems):
        # save audio
        link=audio_elem.get_attribute("src")
        r = requests.get(link, allow_redirects=True)
        file_name=os.path.join(spath,os.path.basename(link))
        open(file_name, 'wb').write(r.content)
        # save arabic
        text = txt_elem.text
        # tafsir
        tzh_elem=tz_elem.find_element_by_xpath(header_xpath)
        header=tzh_elem.text
        text_data=tz_elem.text
        text_data=text_data.replace(header,"")

        _data=f"<header>:{header}<header>\n"
        _data+=f"<text>:{text_data}<text>"
        TZ.append(_data)

        tbh_elem=tb_elem.find_element_by_xpath(header_xpath)
        header=tbh_elem.text
        text_data=tb_elem.text
        text_data=text_data.replace(header,"")

        _data=f"<header>:{header}<header>\n"
        _data+=f"<text>:{text_data}<text>"
        TB.append(_data)
        
        FILES.append(file_name)
        TEXTS.append(text)
        
        xlp_elems=xl_elem.find_elements_by_xpath("p")
        xld=""
        for p in xlp_elems:
            try:
                xlt=p.text
                src=p.find_element_by_xpath(xlsrc_xpath).text
                xld+=f"##:<source>{src}<source><translation>{xlt.replace(src,'')}<translation>\n"
            except NoSuchElementException:
                with open(log_txt,"a+") as f:
                    f.write(f"Translation element incomplete at {driver.current_url} at {xlt}\n")
        TR.append(xld)


def save_surah(i):
    global FILES,TEXTS,TZ,TB,TR
    #Install Driver
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    # get sura
    url = 'https://www.hadithbd.com/quran/tafsir/?sura=' + str(i)
    driver.get(url)
    # sura path
    spath=create_dir(save_dir,str(i))
    csv_path=os.path.join(spath,"data.csv")
    save_data(driver,spath)
    # check if next page exist    
    while check(driver,next_xpath):
        next_link=driver.find_element_by_xpath(next_xpath)
        next_link.click()
        waitSomeTime()
        print(driver.current_url)
        save_data(driver,spath)
        
    df=pd.DataFrame({"filepath":FILES,
                    "text":TEXTS,
                    "tafsir-zakariya":TZ,
                    "tafsir-bayan":TB,
                    "translation":TR})
    df.to_csv(csv_path,index=False)
    FILES=[]
    TEXTS=[]
    TZ=[]
    TB=[]
    TR=[]
    driver.close()



if __name__=="__main__":

    #---------------------------------------------------
    
    for _start in tqdm(range(1,115,batch)):
        _end=_start+batch
        if _end>114:_end=115
        process_list=[]
        for idx in tqdm(range(_start,_end)):
            p =  Process(target= save_surah, args = [idx])
            p.start()
            process_list.append(p)
        for process in process_list:
            process.join()

        
