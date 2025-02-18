import torch.utils.data as tordata
import numpy as np
import os.path as osp
import os
import pickle
import cv2
import xarray as xr
import random
import pickle


class DataSet(tordata.Dataset):
    def __init__(self, seq_dir, label, seq_type, view, cache, resolution):
        self.seq_dir = seq_dir
        self.view = view
        self.seq_type = seq_type
        self.label = label
        self.cache = cache
        self.resolution = int(resolution)
        self.cut_padding = int(float(resolution)/128*20)
        self.data_size = len(self.label)
        self.data = [None] * self.data_size
        self.frame_set = [None] * self.data_size

        self.label_set = set(self.label)
        self.seq_type_set = set(self.seq_type)
        self.view_set = set(self.view)
        _ = np.zeros((len(self.label_set),
                      len(self.seq_type_set),
                      len(self.view_set))).astype('int')
        _ -= 1
        self.index_dict = xr.DataArray(
            _,
            coords={'label': sorted(list(self.label_set)),
                    'seq_type': sorted(list(self.seq_type_set)),
                    'view': sorted(list(self.view_set))},
            dims=['label', 'seq_type', 'view'])

        for i in range(self.data_size):
            _label = self.label[i]
            _seq_type = self.seq_type[i]
            _view = self.view[i]
            self.index_dict.loc[_label, _seq_type, _view] = i

    def load_all_data(self):
        for i in range(self.data_size):
            self.load_data(i)

    def load_data(self, index):
        return self.__getitem__(index)

    def __loader__(self, path):
        return self.pickle2xarray(path).astype('float32') / 255.0
        #return self.img2xarray(path).astype('float32') / 255.0

    def __getitem__(self, index):
        # pose sequence sampling
        if not self.cache:
            data = [self.__loader__(_path) for _path in self.seq_dir[index]]
            frame_set = [set(feature.coords['frame'].values.tolist()) for feature in data]
            frame_set = list(set.intersection(*frame_set))
        elif self.data[index] is None:
            data = [self.__loader__(_path) for _path in self.seq_dir[index]]
            frame_set = [set(feature.coords['frame'].values.tolist()) for feature in data]
            frame_set = list(set.intersection(*frame_set))
            self.data[index] = data
            self.frame_set[index] = frame_set
        else:
            data = self.data[index]
            frame_set = self.frame_set[index]

        return data, frame_set, self.view[
            index], self.seq_type[index], self.label[index],

    def img2xarray(self, file_path):
        imgs = sorted(list(os.listdir(file_path)))
        #print(cv2.imread(osp.join(file_path, imgs[0])).shape)
        frame_list = [np.reshape(
            cv2.imread(osp.join(file_path, _img_path)),
            [self.resolution, self.resolution-2*self.cut_padding, -1])[:, :, 0]
                      for _img_path in imgs
                      if osp.isfile(osp.join(file_path, _img_path))]
        num_list = list(range(len(frame_list)))
        data_dict = xr.DataArray(
            frame_list,
            coords={'frame': num_list},
            dims=['frame', 'img_y', 'img_x'],
        )
        return data_dict

    def pickle2xarray(self, file_path):
        pickles = sorted(list(os.listdir(file_path)))
        frame_list = []
        for _pickle_path in pickles:
            if osp.isfile(osp.join(file_path, _pickle_path)):
                with open(osp.join(file_path, _pickle_path), 'rb') as f:
                    data = pickle.load(f)
                # reshape data if necessary
                frame_list.append(data)
        frame_list = frame_list[0]
        num_list = list(range(len(frame_list)))
        data_dict = xr.DataArray(
            frame_list,
            coords={'frame': num_list},
            dims=['frame', 'pickle_y', 'pickle_x'],
    )
        return data_dict


    def __len__(self):
        return len(self.label)
