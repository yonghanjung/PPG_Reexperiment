# -*- coding: utf-8 -*-
'''
Goal : Download MIMIC data from Physionet
Author : Yonghan Jung, ISyE, KAIST 
Date : 150719 Crawl MIMIC database
Comment 
- 

'''

''' Library '''
import numpy as np
import urllib
import urllib2
from bs4 import BeautifulSoup
import time
''' Function or Class '''


if __name__ == "__main__":
    List_DataNum200 = range(206,295)
    List_DataNum400 = range(400,490)
    List_DataNumTemp = [444]
    Array_DataNum = np.concatenate([List_DataNum200, List_DataNum400])
    # "http://physionet.org/atm/mimicdb/417/417/PLETH/abp/0/60/rdann/annotations.txt"
    # "http://physionet.org/atm/mimicdb/417/417/PLETH_/abp/0/60/rdann/annotations.txt"


    for datanum in List_DataNumTemp:
        if datanum < 100:
            datanum = str(0) + str(datanum)
        else:
            datanum = str(datanum)

        URL_MatFile1 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/PLETH/abp/0/60/export/matlab/" + datanum + "m.mat"
        URL_MatFile2 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/PLETH_/abp/0/60/export/matlab/" + datanum + "m.mat"
        URL_AnnoFile1 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/PLETH/abp/0/60/rdann/annotations.txt"
        URL_AnnoFile2 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/PLETH_/abp/0/60/rdann/annotations.txt"
        URL_InfoFile1 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/" + "PLETH/abp/0/60/export/matlab/" +  datanum + "m.info"
        URL_InfoFile2 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/" + "PLETH2/abp/0/60/export/matlab/" +  datanum + "m.info"
        URL_HeaderFile1 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/PLETH/abp/0/60/export/matlab/"+ datanum + "m.hea"
        URL_HeaderFile2 = "http://physionet.org/atm/mimicdb/" + datanum + "/" + datanum + "/PLETH2/abp/0/60/export/matlab/"+ datanum + "m.hea"

        # Try to read
        GoButton1 = False
        GoButton2 = False
        try:
            HTML1 = urllib2.urlopen(URL_AnnoFile1).read()
            print "True at 1"
            GoButton1 = True
        except:
            print datanum, "1 error"
            GoButton1 = False

        if GoButton1 == False:
            try:
                HTML2 = urllib2.urlopen(URL_AnnoFile2).read()
                print "True at 2"
                GoButton2 = True
            except:
                print datanum, "2 Error"
                GoButton2 = False
                continue

        if GoButton1 == True:
            HTML = HTML1
        elif GoButton2 == True:
            HTML = HTML2


        if GoButton1 == True:
            URL_AnnoFile = URL_AnnoFile1
            URL_MatFile = URL_MatFile1
            URL_InfoFile = URL_InfoFile1
            URL_HeaderFile = URL_HeaderFile1
        elif GoButton2 == True:
            URL_AnnoFile = URL_AnnoFile2
            URL_MatFile = URL_MatFile2
            URL_InfoFile = URL_InfoFile2
            URL_HeaderFile = URL_HeaderFile2

        try:
            Time_Start = time.time()
            urllib.urlretrieve(url=URL_MatFile,filename= datanum + ".mat")
            urllib.urlretrieve(url=URL_AnnoFile,filename= datanum + "_Anno.txt")
            urllib.urlretrieve(url=URL_InfoFile,filename= datanum + "_Info.txt")
            urllib.urlretrieve(url=URL_HeaderFile,filename= datanum + "_Head.txt")
            print datanum, "successfully downloaded in given time"

        except:
            print datanum, "Failed to download"
            continue



