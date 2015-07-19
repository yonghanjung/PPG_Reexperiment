

__author__ = 'jeong-yonghan'

def data_call(data_name, data_num, wanted_length):
    import scipy.io
    import numpy as np
    from compiler.ast import flatten
    if data_name == "PPG":
        if data_num == 1:
            mysignal = scipy.io.loadmat("Data/mynewsignal")
            mysignal = mysignal['mysignal']
            mysignal = np.array(mysignal).tolist()
            mysignal = flatten(mysignal)
            if wanted_length == 0:
                pass
            else:
                mysignal = mysignal[:wanted_length]
            return mysignal
        else:
            mysignal = scipy.io.loadmat("Data/mynewdata" + str(data_num))
            mysignal = mysignal['mysignal' + str(data_num)]
            mysignal = np.array(mysignal).tolist()
            mysignal = flatten(mysignal)
            if wanted_length == 0:
                pass
            else:
                mysignal = mysignal[:wanted_length]
            return mysignal

    if data_name == "PPG_KW":
        if data_num == 1:
            mysignal = scipy.io.loadmat("../Data/mytest.mat")
            mysignal = mysignal['var']
            mysignal = mysignal[0]
            mysignal = np.array(mysignal).tolist()
            mysignal = flatten(mysignal)
            if wanted_length == 0:
                pass
            else :
                mysignal = mysignal[:wanted_length]
            return mysignal
        else:
            mysignal = scipy.io.loadmat("../Data/mytest" + str(data_num))
            mysignal = mysignal['var' + str(data_num)]
            mysignal = np.array(mysignal).tolist()
            mysignal = flatten(mysignal)
            if wanted_length == 0:
                pass
            else :
                mysignal = mysignal[:wanted_length]
            return mysignal

    if data_name == "PPG_KW_long":
        file = open("../Data/" + str(data_num) + ".txt",'r')
        mydata = file.read().split(' ')
        mydata = filter(lambda x: len(x)>0, mydata)
        mydata = [int(x) for x in mydata]
        if wanted_length == 0:
            pass
        else :
            mydata = mydata[:wanted_length]
        return mydata

    if data_name == "PPG_Walk":
        file = open("../Data/" + data_name + str(data_num) + ".txt",'r')
        mydata = file.read().split('\t')
        mydata = filter(lambda x: len(x)>0, mydata)
        mydata = [float(x) for x in mydata]
        if wanted_length == 0:
            pass
        else :
            mydata = mydata[:wanted_length]
        return mydata

    # if data_name == "PPG_MIMIC":


    if data_name == "ECG_HE":
        mysignal = scipy.io.loadmat("../Data/ECG_HE.mat")
        mysignal = mysignal['ECG_HE']
        mysignal = mysignal[data_num]
        mysignal = np.array(mysignal).tolist()
        mysignal = flatten(mysignal)
        if wanted_length == 0:
            pass
        else :
            mysignal = mysignal[:wanted_length]
        return mysignal

    if data_name == "ECG_MI":
        mysignal = scipy.io.loadmat("../Data/ECG_MI.mat")
        mysignal = mysignal['ECG_MI']
        mysignal = mysignal[data_num]
        mysignal = np.array(mysignal).tolist()
        mysignal = flatten(mysignal)
        if wanted_length == 0:
            pass
        else :
            mysignal = mysignal[:wanted_length]
        return mysignal

