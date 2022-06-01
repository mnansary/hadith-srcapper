#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
from .core import *
from .constants import *
import json

def get_text(elem,xpath):
    if check(elem,xpath):
        sub_elem=elem.find_element_by_xpath(xpath)
        return sub_elem.text
    else:
        return None


def save_data_url(url,driver,json_path):
    main={}
    _dict={}
    #  load
    driver.get(url)
    # check for explanation button
    if check(driver,xpaths.explanation):
        elem=driver.find_element_by_xpath(xpaths.explanation)
        if len(elem.text)==0:
            if check(driver,xpaths.exp_button):
                button=driver.find_element_by_xpath(xpaths.exp_button)
                clickLink(button)
                elem=driver.find_element_by_xpath(xpaths.explanation)
                _dict["explanation"]=elem.text
            else:
                _dict["explanation"]=None
        else:
            _dict["explanation"]=elem.text
    else:
        _dict["explanation"]=None
    
    # arabic
    _dict["arabic"]=get_text(driver,xpaths.arabic)
    # bangla
    _dict["bangla"]=get_text(driver,xpaths.bangla)
    # narrator
    _dict["narrator"]=get_text(driver,xpaths.narrator)
    # validuty
    _dict["validity"]=get_text(driver,xpaths.validity)
    # extra note
    _dict["extra-note"]=get_text(driver,xpaths.extra_note)
    # header
    meta={}
    if check(driver,xpaths.chapter):
        link=driver.find_element_by_xpath(xpaths.chapter)
        header=link.find_element_by_xpath("h3")
        prefaces=link.find_elements_by_xpath("p")
        pref_texts=[]
        for elem in prefaces:
            pref_texts.append(elem.text)
        meta["header"]=header.text
        meta["preface"]=pref_texts
    else:
        meta["header"]=None
        meta["preface"]=None
    main["meta"]=meta
    main["data"]=_dict
    with open(json_path, 'w') as fp:
        json.dump(main, fp,sort_keys=True, indent=4,ensure_ascii=False)
            
    
    
    
    
    


