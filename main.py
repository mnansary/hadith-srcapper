# -*-coding: utf-8 -
'''
    @author:  MD. Nazmuddoha Ansary
'''
#--------------------
# imports
#--------------------
from core.utils import create_dir,LOG_INFO
from core import launchBrowser,save_data_url
import os 
from tqdm import tqdm
#--------------------
# main
#--------------------
def main(url,start,end,save_path,iden):
    LOG_INFO(f"url:{url},start:{start},end:{end},iden:{iden}")
    driver=launchBrowser()
    save_path=create_dir(save_path,iden)
    for i in tqdm(range(start,end+1)):
        dataurl=f"{url}/{i}"
        json_path=os.path.join(save_path,f"{i}.json")
        save_data_url(dataurl,driver,json_path)
    driver.close()
#-----------------------------------------------------------------------------------

if __name__=="__main__":
    url="http://ihadis.com/books/bukhari/hadis"
    start=1
    end=10
    main(url,start,end,"../../","bukhari")
    
    