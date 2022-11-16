# -*-coding: utf-8 -
'''
    @author:  MD. Nazmuddoha Ansary
'''
#--------------------
# imports
#--------------------
import argparse
import os 
from core.utils import create_dir,LOG_INFO
from core import launchBrowser,save_data_url
from multiprocessing import Process
from tqdm import tqdm
#--------------------
# functions
#--------------------
def run(url,start,end,save_path,iden):
    LOG_INFO(f"url:{url},start:{start},end:{end},iden:{iden}")
    driver=launchBrowser()
    if driver is not None:
        save_path=create_dir(save_path,iden)
        for i in tqdm(range(start,end+1)):
            dataurl=f"{url}/{i}"
            json_path=os.path.join(save_path,f"{i}.json")
            save_data_url(dataurl,driver,json_path)
        driver.close()


def execute(start,end,batch,url,iden,save_path):
    '''
        multiprocessing
    '''
    process_list=[]
    for _start in range(start,end,batch):
        _end=_start+batch-1
        if _end>end:_end=end
        p =  Process(target= run, args = [url,_start,_end,save_path,iden])
        p.start()
        process_list.append(p)
    for process in process_list:
        process.join()


def main(args):
    start       =   int(args.start)
    end         =   int(args.end)
    save_path   =   args.save_path
    iden        =   args.iden
    batch       =   int(args.batch)
    # run and execute
    url=f"http://ihadis.com/books/{iden}/hadis"
    execute(start,end,batch,url,iden,save_path)

if __name__=="__main__":

    '''
        parsing and execution
    '''
    parser = argparse.ArgumentParser("ihadith website scrapper")
    parser.add_argument("iden", help="book name from the website")
    parser.add_argument("end", help="end of hadith no to sracpe from the book")
    parser.add_argument("save_path", help="path to save the json data [the provided iden will be used to create a folder]")
    parser.add_argument("--start",required=False,default=1,help="start of hadith no to scrape from the book")
    parser.add_argument("--batch",required=False,default=500,help="batch number for multiprocessing [1 process will be allocated for n number of hadiths]")
    
    args = parser.parse_args()
    main(args)
    

    