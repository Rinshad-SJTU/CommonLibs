import numpy as np
import matplotlib.pyplot as plt

def blocks_to_image(blocks,index,hight_num=20,weight_num=20):
    c=0
    h=hight_num
    w=weight_num
    j=c%(h*w)
    
    for i in index:
        if j==0:
            tmpim=np.zeros([blocks.shape[1]*w,blocks.shape[2]*h,blocks.shape[3]])
        tmpim[(j%w)*blocks.shape[1]:(j%w)*blocks.shape[1]+blocks.shape[1],\
          int(j/w)*blocks.shape[2]:int(j/w)*blocks.shape[2]+blocks.shape[2],:]=blocks[i,:,:,:]                   
        c=c+1
        j=c%(h*w)
        
    return tmpim


import class_interface as libci
def image_to_blocks(image,radius=16,angles=[0],stride=4,pyramid=1):
    #return image blocks and ids{centroid,radius,angle}
    l=len(range(radius,image.shape[0]-radius,stride))*len(range(radius,image.shape[1]-radius,stride))
    block_shape=(l,2*radius,2*radius,image.shape[2])
    image_blocks=np.ndarray(shape=block_shape)
    ids=[0]*l
    index=0
    for i in range(radius,image.shape[0]-radius,stride):
        for j in range(radius,image.shape[1]-radius,stride):
            block_im=image[i-radius:i+radius,j-radius:j+radius,:]
            image_blocks[index,:,:,:]=block_im
            block_id={}
            block_id['centroid']=(i,j)
            block_id['radius']=radius
            block_id['angle']=angles[0]
            ids[index]=libci.Dic2Object(block_id)
            index+=1
    
    return image_blocks,ids

def image_to_blocksinfo(image,radius=16,angles=[0],stride=4,pyramid=1):
    '''
    return ids and block shape
    '''
    l=len(range(radius,image.shape[0]-radius,stride))*len(range(radius,image.shape[1]-radius,stride))
    block_shape=(l,2*radius,2*radius,image.shape[2])
    ids=[0]*l
    index=0
    for i in range(radius,image.shape[0]-radius,stride):
        for j in range(radius,image.shape[1]-radius,stride):
            block_id={}
            block_id['centroid']=(i,j)
            block_id['radius']=radius
            block_id['angle']=angles[0]
            ids[index]=libci.Dic2Object(block_id)
            index+=1
    return ids,block_shape

import cv2
def get_block_fromids(image,ids,block_size):    
    i,j=ids.centroid
    block_shape=(block_size[0],block_size[1],image.shape[2])
    tmp_image=image[i-ids.radius:i+ids.radius,j-ids.radius:j+ids.radius]
    image_block=np.ndarray(shape=block_shape)
    for i in range(image.shape[2]):
        image_block[:,:,i]=cv2.resize(tmp_image[:,:,i],block_shape[0:2])
    return image_block

    
def save_figure(file_path):
    plt.savefig(file_path)

def plot_figure(n,max_n,rows,cols,data):
    plt.figure(figsize=(cols*5,rows*5))
    for i in range(rows):
        for j in range(cols):
            index=i*cols+j
            plt.subplot(rows, cols, index+1)
            plt.plot(data[index][:n])
            plt.grid()
            plt.axis([0,max_n ,min(data[index][:n])*0.9,max(data[index][:n])*1.1])