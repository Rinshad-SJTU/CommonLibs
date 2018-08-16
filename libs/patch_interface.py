import scipy.io as sio
import numpy as np
# datafile = '../data_before.mat'
# datafile = './ag_data.npy'
# labelfile= './ag_label.npy'
# datafile='./dnn_data.npy'
# labelfile='./label.npy'
data_x =np.zeros([])# np.load(datafile)
data_y=np.zeros([])#np.load(labelfile)
datalength = 0#data_y.size
dataindex =[]# np.arange(datalength)
train_ids=[]
val_ids=[]

#========================================>
#将所有数据分为训练集和验证集
proportion = 0.7
# s = np.int(datalength * proportion)
# train_ids = dataindex[:s]
# val_ids = dataindex[s:]

def update_index(train_proportion=0.7):
    global proportion
    proportion=train_proportion
    global datalength
    datalength=data_y.shape[0]
    global dataindex
    dataindex =np.arange(datalength)
    shuffle()
    partitiondataset(proportion)

def load_from_file(file_path,name_x='x',name_y='y'):
    loaded=np.load(file_path)
    global data_x,data_y
    data_x = loaded[name_x]
    data_y = loaded[name_y]
    update_index(0.8)
    
#read image from mat file
def read_data(dataids,to_categorical=False):
    imgs = []
    labels = []
    for num in dataids:
        img=data_x[num].astype(np.float).reshape([32,32,3])
        imgs.append(img)
        if to_categorical:
            tmp=[0,0]
            tmp[1]=1-data_y[num]
        else:
            tmp=[0]
        
        tmp[0]=data_y[num]
        #   
        labels.append(tmp) 

    return np.asarray(imgs, np.float), np.asarray(labels, np.float).reshape((-1,1)), np.asarray(dataids, np.int)

#定义一个函数，按批次取数据


def minibatches(input=None, batch_size=None, shuffle=False,to_categorical=False):
    if shuffle:
        indices = np.arange(len(input))
        np.random.shuffle(indices)

    for start_idx in range(0, len(input) - batch_size + 1, batch_size):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batch_size]
        else:
            excerpt = slice(start_idx, start_idx + batch_size)
        yield read_data(input[excerpt],to_categorical)


#打乱顺序
def shuffle():
    global dataindex
    np.random.shuffle(dataindex)

def partitiondataset(radio = 0.8):
    global proportion
    proportion=radio
    global datalength
    global train_ids,val_ids,dataindex
    s = np.int(datalength * radio)
    train_ids = dataindex[:s]
    val_ids = dataindex[s:]


