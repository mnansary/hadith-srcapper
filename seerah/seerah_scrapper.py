#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
from time import sleep

import sys
sys.path.append('..')
from core.core import *
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
# ---------------------------------------------------------
# globals
# ---------------------------------------------------------
URL         =   "https://arqadhi.blogspot.com/"
LINK_XPATH  =   './/div[@class="widget-content"]/ul/li/a'
TEXT_XPATH  =   './/div[@class="post-body entry-content"]'
TITLE_XPATH =   './/h3[@class="post-title entry-title"]'

# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    driver=launchBrowser(Debug=False)
    driver.get(URL)

    # get all list of links of scrapable data
    link_elems=driver.find_elements_by_xpath(LINK_XPATH)
    LINKS=[]
    for elem in link_elems:
        LINKS.append(elem.get_attribute("href"))
    
    ids   =[]
    urls  =[]
    titles=[]
    texts =[]
    infos =[]
    # scrape
    for url in tqdm(LINKS):
        try:
            driver.get(url)
            if check(driver,TEXT_XPATH):
                title=driver.find_element_by_xpath(TITLE_XPATH).text
                text_elem=driver.find_element_by_xpath(TEXT_XPATH)
                text=text_elem.text
                parts=text.split("\n\n[Transcribed")
                main_text=parts[0].replace("[DOWNLOAD MP3]\n\n",'')
                transcription_info="[Transcribed"+parts[-1]
                ids.append(title.split("-")[0])
                urls.append(url)
                titles.append(title)
                texts.append(main_text)
                infos.append(transcription_info)
        except Exception as e:
            print(url)
    df=pd.DataFrame({"id":ids,"url":urls,"title":titles,"text":texts,"transcription":infos})
    df.to_csv("seerah.csv",index=False)

    driver.close()

if __name__=="__main__":
    main()

    
        
