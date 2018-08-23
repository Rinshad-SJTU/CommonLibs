import numpy as np
import matplotlib.pyplot as plt
import sys
if __name__=='__main__':
    import platform
    import sys
    if platform.system()=='Windows':
        sys.path.append(u'../')
        sys.path.append(u'F:\IIAI\CommonLibs\libs')
    elif platform.system()=='Linux':
        sys.path.append('../')
        sys.path.append('/home/sheldon/Documents/Code/CommonLib/')


import file_interface as libfi        
import view_interface as libvi

def split_data_set(label,radio=0.7):
    '''
    split data set to train set and test set
    radio is the present of train set
    '''
    label_set=set(label)
    train_index=set([])
    test_index=set([])
    for i in list(label_set):
        index=np.where(label==i)[0]
        s=index.size
        np.random.shuffle(index)
        train_index=train_index|set(index[:round(s*radio)])
        test_index=test_index|set(index[round(s*radio):])

    return list(train_index),list(test_index)

class mutil_npzfile_reader:
    """
    file_dics:
        file的关键key和路径
    args:
        增强的参数：
            --angle_gap:旋转间隔角度
            --stride:块的间隔步长
            --radius:图像块的半径
        ids属性:
            --angle:旋转角度
            --centroid:图像块中心
            --radius:图像块的半径
    block_shape:
        图像块的形状
    dtype:
        图像数据的类型
    """
    def __init__(self,file_dics,args,block_shape,dtype=None,transform_fn=None):
        self._index2ids=None#索引到ids的list
        self._genindex_(file_dics,args)
        self._shape=[len(self._index2ids)]
        self._shape+=block_shape[:]
        self._transform_fn=transform_fn
        if dtype is None:
            self._dtype=np.float32
        else:
            self._dtype=dtype
        self._in_memory={}
        self._file_dics=file_dics
        for key in file_dics:
            self._in_memory[key]=False
            
        self._cache=None
        self._current_key=None
    
    def _read_file(self, key):
        if not self._in_memory[key]:
            if self._current_key is not None:
                self._in_memory[self._current_key]=False
                self._cache=None

            self._current_key=key
            if self._transform_fn is not None:
                self._cache=self._transform_fn(self._file_dics[key])
            else:
                self._cache=np.load(self._file_dics[key])['data']

    def __getitem__(self,index):
        if type(index) is list:
            result=[]
            for i in index:
                result.append(self.__getitem_byids__(self._index2ids[i]))
        else:
            result=[self.__getitem_byids__(self._index2ids[index])]
        return result

    def _genindex_(self,image_dics,args):
        for key in image_dics:
            loaded=np.load(image_dics[key])
            ids=loaded['ids']
            # ids,_=libvi.image_to_blocksinfo(im,radius=args.radius,stride=args.stride)
            for i in range(len(ids)):
                ids[i].file_key=key
                ids[i].index=i

            if self._index2ids is None:
                self._index2ids=ids.tolist()
            else:
                self._index2ids+=ids.tolist()[:]

    def __getitem_byids__(self,ids):
        self._read_file(ids.file_key)
        result=self._cache[ids.index]
        return result


    @property
    def dtype(self):
        return self._dtype
    @property
    def shape(self):
        return self._shape

    def __len__(self):
        return len(self._index2ids)

import cv2 
class mutil_image_reader:
    """
    image_dics:
        图像的关键key和路径
    args:
        图像增强的参数：
            --angle_gap:旋转间隔角度
            --stride:块的间隔步长
            --radius:图像块的半径
        ids属性:
            --angle:旋转角度
            --centroid:图像块中心
            --radius:图像块的半径
    block_shape:
        图像块的形状
    dtype:
        图像数据的类型
    """
    def __init__(self,image_dics,args,block_shape,dtype=None,transform_fn=None):
        self._index2ids=None#索引到ids的list
        self._genindex_(image_dics,args)
        self._shape=[len(self._index2ids)]
        self._shape+=block_shape[:]
        self._transform_fn=transform_fn
        if dtype is None:
            self._dtype=np.float32
        else:
            self._dtype=dtype
        self._in_memory={}
        self._image_dics=image_dics
        for key in image_dics:
            self._in_memory[key]=False
            
        self._cache=None
        self._current_key=None
    
    def _read_file(self, key):
        if not self._in_memory[key]:
            if self._current_key is not None:
                self._in_memory[self._current_key]=False
                self._cache=None

            self._current_key=key
            if self._transform_fn is not None:
                self._cache=self._transform_fn(self._image_dics[key])
            else:
                self._cache=np.load(self._image_dics[key])

    def __getitem__(self,index):
        if type(index) is list:
            result=[]
            for i in index:
                result.append(self.__getitem_byids__(self._index2ids[i]))
        else:
            result=[self.__getitem_byids__(self._index2ids[index])]
        return result

    def _genindex_(self,image_dics,args):
        for key in image_dics:
            img=cv2.imread(image_dics[key])
            ids,_=libvi.image_to_blocksinfo(img,radius=args.radius,stride=args.stride)
            for i in range(len(ids)):
                ids[i].file_key=key

            if self._index2ids is None:
                self._index2ids=ids
            else:
                self._index2ids+=ids[:]

    def __getitem_byids__(self,ids):
        self._read_file(ids.file_key)
        result=libvi.get_block_fromids(image=self._cache,ids=ids,block_size=self.shape[1:3])
        return result


    @property
    def dtype(self):
        return self._dtype
    @property
    def shape(self):
        return self._shape

    def __len__(self):
        return len(self._index2ids)


if __name__=='__main__':
    import platform 
    if platform.system()=='Linux':
        image_dir='/home/sheldon/Documents/Data/YiZhou/idrid/Original_Images/Training_Set'
        export_image_dir='/home/sheldon/Documents/Code/IIAI/tmp_tool/result/{name}.jpg'
        data_dic=libfi.getfiledicbyext(image_dir,'.jpg|.jpeg|.bmp|.png')
    elif platform.system()=='Windows':
        image_dir=u'C:\\Users\\SeldomRiver\\Pictures\\Saved Pictures'
        export_image_dir=u'C:\\Users\\SeldomRiver\\Pictures'
        data_dic=libfi.getfiledicbyext(image_dir,'.jpg|.jpeg|.bmp|.png')

    import cv2
    def _readimage(file_path):
        im=cv2.imread(file_path).astype(np.float)/255.0
        return im
    import argparse as ag
    c=ag.ArgumentParser()
    c.add_argument('--radius')
    c.add_argument('--stride')
    c.add_argument('--angle_gap')
    c.radius=32
    c.stride=4
    c.angle_gap=30
    data=mutil_image_reader(image_dics=data_dic,args=c,block_shape=[64,64,3],transform_fn=_readimage)
    print(len(data))
    import matplotlib.pyplot as plt
    i=list(range(1000,100000,1000))
    ims=data[i]
    for i in range(len(ims)):
        im=ims[i]
        cv2.imwrite(export_image_dir.format(name=i),(im*255.0).astype(np.uint8))
    # for i in range(1000,1500,1):
    #     im=data[i]
    #     cv2.imwrite(export_image_dir.format(name=i),(im[0]*255.0).astype(np.uint8))
