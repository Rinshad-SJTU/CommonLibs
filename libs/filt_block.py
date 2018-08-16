import numpy as np
import matplotlib.pyplot as plt
if __name__=='__main__':
    file_path='./tmp_data/train-data.npz'
    tar_file_path='./tmp_data/filted-train-data.npz'
    loaded=np.load(file_path)
    data=loaded['x']
    label=loaded['y']
    sums=np.sum(np.sum(np.sum(data,axis=3),axis=2),axis=1)
    r_data=data[sums>400,:,:,:]
    r_label=label[sums>400,:]
    print(np.sum(r_label))
    print(np.sum(label))
    np.savez_compressed(tar_file_path,x=r_data,y=r_label)