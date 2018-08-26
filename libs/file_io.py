#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os.path
import numpy as np
import time
import datetime
defaultext = '.npz'

class fileStreamer:
    def __init__(self, fdir, fid):
        self._filepath=None
        self.updatefilepath(fdir, fid)
        self.__lastmodifytime=None
        self._candidate = None
        self._label = None
        self._region = None
        self._img_eq = None

    def initdata(self,region,candidate,labels,img_eq):
        self._img_eq=img_eq
        self._label=labels
        self._region=region
        self._candidate=candidate
        self.__datamodified()

    def getdata(self):
        '''
        return region, label, candidate, img_eq
        '''
        if not self.is_in_memory():
            self.read()
        return (self._region,self._label,self._candidate,self._img_eq)

    def __datamodified(self):
        self.__lastmodifytime=time.time()

    def updateLabel(self,new_label):
        self._label=new_label
        self.__datamodified()

    def get_filepath(self):
        return self._filepath

    def _filemodifytime(self):
        if not self.exist():
            return None
        loaded = np.load(self._filepath)
        if 'time_stamp' in loaded.keys():
            return loaded['time_stamp']
        else:
            return None

    def save(self, targetFile=None):
        if targetFile is None:
            targetFile = self._filepath

        if self.is_in_memory():
            tmp=self._filemodifytime()
            if tmp is None or self.__lastmodifytime>tmp:
                np.savez_compressed(targetFile,
                region=self._region,
                label=self._label,
                fileId=self._fileId,
                candidate=self._candidate,
                img_eq=self._img_eq,
                time_stamp=self.__lastmodifytime)

    def read(self, FilePath=None):
        if FilePath is None:
            if self.exist():
                loaded = np.load(self._filepath)
        elif os.path.exists(FilePath):
            loaded = np.load(FilePath)
            (filepath, tempfilename) = os.path.split(FilePath)
            self.updatefilepath(filepath, tempfilename)

        self.__selized_data__(loaded)

    def updatefilepath(self, folder, fileid):
        if fileid[-4:].lower() != defaultext:
            self._filepath = folder + '/' + fileid + defaultext
            self._fileId = fileid
        else:
            self._filepath = folder + '/' + fileid
            self._fileId = fileid[:-4]

    def exist(self):
        return os.path.exists(self._filepath)

    def __clear_mem__(self):
        self._candidate = None
        self._label = None
        self._region = None
        self._img_eq = None

    def trans_to_file(self):
        self.save()
        self.__clear_mem__()

    def load_from_file(self):
        if self.exist():
            loaded = np.load(self._filepath)
            self.__selized_data__(loaded)
            return True
        else:
            return False

    def __selized_data__(self, data):
        self._fileId = data['fileId'].item()
        self._region = data['region']
        self._label = data['label']
        self._candidate = data['candidate']
        if 'img_eq' in data.keys():
            self._img_eq = data['img_eq'].astype(np.uint8)
        else:
            self._img_eq = None
            
        if 'time_stamp' in data.keys():
            self.__lastmodifytime=data['time_stamp']
        else:
            self.__lastmodifytime=time.time()

    def is_in_memory(self):
        return self._region is not None
