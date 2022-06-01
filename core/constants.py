#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function

# ---------------------------------------------------------
# class for Scripts
# ---------------------------------------------------------
class SCRIPTS:

    scrollElementIntoMiddle =   "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"\
                                            + "var elementTop = arguments[0].getBoundingClientRect().top;"\
                                            + "window.scrollBy(0, elementTop-(viewPortHeight/2));"

    scrollHeight            =   "return document.body.scrollHeight"
    
    scroll                  =   "window.scrollTo(0, document.body.scrollHeight);"

    click                   =   "arguments[0].click();"

    scrollDiv               =   "arguments[0].scrollIntoView(false);"
    
    scrollDivShow           =   "arguments[0].scrollIntoView(true);"

# ---------------------------------------------------------
# class for Xpaths
# ---------------------------------------------------------
class xpaths:
    # xpaths for page data
    arabic      ='.//p[@class="hadith-des2"]'
    narrator    ='.//p[@class="narrated-by"]'
    bangla      ='.//p[@class="hadith-des"]'
    explanation ='.//div[@class="row hadis-extra collapsed explanation"]'    
    exp_button  ='.//*[@class="explanation hidden-print"]'
    chapter     ='.//div[@class="chapter hidden-print"]'
    validity    ='.//span[@class="label validity"]'
    extra_note  ='.//div[@class="row hadis-extra note"]'
