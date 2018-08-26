
import os.path as osp
import numpy as np
# my libs
import libs.file_interface as libfi
import libs.file_io as libio
import libs.view_interface as libvi
import deepnetwork.preprocess as dnnprep
import matplotlib.pyplot as plt
import libs.data_interface as libsdi
import parms as p


class model_data:
    def __init__(self, file_path):
        self.__file = file_path
        self.__data = None
        self.__label = None

    def file_exist(self):
        return osp.exists(self.file_path) or self.__data is not None 

    def get_file_path(self):
        return self.__file
    file_path = property(get_file_path)

    def save_to_file(self):
        if self.__data is not None:
            np.savez_compressed(self.file_path, x=self.__data, y=self.__label)
            self.__train_data = None
            self.__train_label = None

    def load_from_file(self):
        loaded = np.load(self.file_path)
        self.__data = loaded['x']
        self.__label = loaded['y']
        return self.__data, self.__label

    def __in_memory(self):
        return self.__data is not None

    def get_data(self):
        if self.__in_memory():
            return self.__data, self.__label
        elif self.file_exist():
            self.load_from_file()
            return self.__data, self.__label
        else:
            raise FileNotFoundError(self.file_path)


class data_manager:
    def __init__(self, fun_getFeature = None):
        '''
        fun_getFeature : data,label=fun(key,file_path)
        '''
        self.__train_data_model = model_data(p.train_data_file)
        self.__test_data_model = model_data(p.test_data_file)
        self.__all_data_model = model_data(p.all_data_file)
        self.__feature_handle=fun_getFeature

    def _merge_data_from_seq_files(self):
        '''
        '''
        if not self.__all_data_model.file_exist():
            sep_files = libfi.getfiledicbyext(p.sep_file_dir, ext=p.sep_file_ext)
            data_files = libfi.getfiledicbyext(p.data_file_dir, ext=p.data_file_ext)
            for num,key in enumerate(sep_files):
                print(num,':',sep_files[key])
                if key not in data_files:
                    print('feature gen : ',key)
                    data,label=self.__feature_handle(sep_files[key])
                    np.savez_compressed(p.data_file_dir+'/'+key+p.data_file_ext,x=data,y=label)

            all_data = []
            all_label = []
            data_files = libfi.getfiledicbyext(p.data_file_dir, ext=p.data_file_ext)
            for num, file_path in enumerate(data_files):
                print(num + 1, ':', file_path)
                try:
                    loaded = np.load(file_path)
                    data = loaded['x']
                    label = loaded['y']
                    all_data.append(data)
                    all_label.append(label)
                except Exception as exp:
                    print('Exception:', exp)
                    print('data path:' + file_path)
                    continue
            all_data = np.ndarray(all_data)
            all_label = np.ndarray(all_label)
            np.savez_compressed(
                self.__all_data_model.file_path, x=all_data, y=all_label)

    def _split_dataset(self):
        data,label=self.__all_data_model.get_data()
        train_index,test_index=libsdi.split_data_set(label,p.radio)
        np.savez_compressed(self.__train_data_model.file_path,x=data[train_index],y=label[train_index])
        np.savez_compressed(self.__test_data_model.file_path,x=data[test_index],y=label[test_index])

    def get_train_data(self):
        '''
        return train dataset
        data : train data,  size = (n,:,:,:)
        label: train data labels, size = (n,1)
        '''
        if not self.__train_data_model.file_exist():
            self.merge_data_from_seq_files()
            self._split_dataset()
            
        data,label = self.__train_data_model.get_data()
        return (data, label)

    def get_test_data(self):
        '''
        return train dataset
        data : train data,  size = (n,:,:,:)
        label: train data labels, size = (n,1)
        '''
        if not self.__test_data_model.file_exist():
            self.merge_data_from_seq_files()
            self._split_dataset()
            
        data,label = self.__test_data_model.get_data()
        return (data, label)
