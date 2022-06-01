# -*-coding: utf-8 -
'''
    @author:  MD. Nazmuddoha Ansary
'''
#--------------------
# imports
#--------------------
from main import main
from multiprocessing import Process
url="http://ihadis.com/books/muslim/hadis"
start=1
end=7500
save_path="../../"
iden="muslim"
batch=500
#--------------------
# main
#--------------------
if __name__=="__main__":
    process_list=[]
    for _start in range(start,end,batch):
        _end=_start+batch-1
        if _end>end:_end=end
        p =  Process(target= main, args = [url,_start,_end,save_path,iden])
        p.start()
        process_list.append(p)
    for process in process_list:
        process.join()


    