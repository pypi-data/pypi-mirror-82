#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
FeatureUtil

Authors: wangkai02(wangkai02@corp.netease.com)

Phone: 17816029211

Date: 2019/9/11

Authors: zouzhene(zouzhene@corp.netease.com)

Phone: 13261632788

Date: 2020/3/11
"""
from tensorflow.python.data.ops import dataset_ops
import tensorflow as tf
import numpy as np
import re
import scipy
from tensorflow.python.keras.preprocessing import sequence


class FeatureUtil:
    '''
    构建数据集的工具类，构建的数据集以本地文件的方式进行存储。
    目前支持两种数据存储格式：tfrecord 和 hdf5。

    Args:
        config: 配置文件，定义了如下一些属性：
                    序列数量、

                    序列最大长度
    '''

    def __init__(self, config):
        self.config = config
        self.maxlen = config['maxlen']
        self.batchsize = config['batchsize']
        self.class_num = config['class_num']
        self.cross_feature_num = config['cross_feature_num']
        self.user_feature_num = config['user_feature_num']
        self.user_feature_size = config['user_feature_size']
        self.output_unit = config['output_unit']
        self.multi_class = config['multi_class']
        self.neg_sample = config['neg_sample']
        self.seq_num = self.config['seq_num']

    def feature_extraction(self, data, predict=False, h5=False):
        '''
        从原始数据中提取特征，后续调用不同的方法将特征存储为 tfrecord 或者 hdf5 格式。

        Args:
            data: 原始数据
            predict: 是否预测阶段
            h5: 是否 hdf5 格式，默认为 tfrecord

        Returns:
            特征数据
        '''
        feature_id = {
            'role_id': 0,
            'role_id_hash': 1,
            'sequence_feature': 2,
            'cross_feature': 3,
            'user_feature': 4,
            'pos_label': 5,
            'neg_label': 6,
            'cur_time': 7,
            'weight': 8
        }

        role_id = [[int(sample.split('@')[feature_id['role_id']])] for sample in data]
        role_id_hash = [int(sample.split('@')[feature_id['role_id_hash']]) for sample in data]
        # pos_label = [int(sample.split('@')[feature_id['pos_label']].split(':')[0]) for sample in data]

        pos_label = [[x for x in map(int, sample.split('@')[feature_id['pos_label']].split(','))] for sample in data]
        neg_label = [[x for x in map(int, sample.split('@')[feature_id['neg_label']].split(','))] for sample in data]
        mask = [[x for x in set(pos_label[i] + neg_label[i])] for i in range(len(data))]

        cur_time = [int(sample.split('@')[feature_id['cur_time']]) for sample in data]

        sequence_id = [
            [[int(x.split(':')[0]) for x in
              sorted(re.split(', |,', xx), key=lambda x: x.split(':')[-1])][-self.maxlen:] if xx else [0] for xx in
             sample.split('@')[feature_id['sequence_feature']].split(';')[:self.seq_num]]
            for sample in data]
        sequence_time = [
            [[int(sample.split('@')[feature_id['cur_time']]) - int(x.split(':')[1]) for x in
              sorted(re.split(', |,', xx), key=lambda x: x.split(':')[-1])][-self.maxlen:] if xx else [0] for xx in
             sample.split('@')[feature_id['sequence_feature']].split(';')[:self.seq_num]]
            for sample in data]
        sequence_time_gaps = [[[0] + [abs(xx[i] - xx[i - 1]) for i in range(1, len(xx))] for xx in sample] for sample in sequence_time]

        cross_features_index = [[int(y.split(':')[0]) for y in re.split(', |,', sample.split('@')[feature_id['cross_feature']])] for sample in data]  # id+maxid*daygap
        cross_features_val = [[float(y.split(':')[1]) for y in re.split(', |,', sample.split('@')[feature_id['cross_feature']])] for sample in data]  # value
        user_features_id = [[int(y) if y else 0 for y in re.split(', |,', sample.split('@')[feature_id['user_feature']])] for sample in data]  # id+maxid*daygap
        user_features_id = [sample + [0] * (self.user_feature_num - len(sample)) for sample in user_features_id]
        # label_week_id = [[int(data[i].split('@')[feature_id['pos_label']].split(':')[1])] * len(sequence_id[i]) for i in range(len(data))]

        if h5:
            cross_features_index = [np.array(item, dtype=np.int64) for item in cross_features_index]
            cross_features_val = [np.array(item, dtype=np.float32) for item in cross_features_val]
            sequence_id = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_id]
            sequence_time = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_time]
            sequence_time_gaps = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_time_gaps]
            return np.array(role_id_hash, dtype=np.int64), np.array(sequence_id, dtype=np.int64), \
                   np.array(sequence_time, dtype=np.int64), np.array(sequence_time_gaps, dtype=np.int64), \
                   cross_features_index, cross_features_val, \
                   np.array(user_features_id, dtype=np.int64), np.array(cur_time, dtype=np.int64), np.array(pos_label)

        if predict:
            cross_features_index = [[[i, int(y.split(':')[0])] for y in re.split(', |,', sample.split('@')[feature_id['cross_feature']])] for i, sample in enumerate(data)]
            cross_features_index, cross_features_val = self.cross_features_batch(cross_features_index, cross_features_val)
            sequence_id = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_id]
            sequence_time = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_time]
            sequence_time_gaps = [sequence.pad_sequences(x, maxlen=self.maxlen, padding='post') for x in sequence_time_gaps]
            return np.array(role_id_hash), np.array(sequence_id), np.array(sequence_time), np.array(sequence_time_gaps), \
                   np.array(cross_features_index), np.array(cross_features_val), np.array(user_features_id), np.array(cur_time)

        return role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val, user_features_id, pos_label, neg_label, mask, cur_time

    def cross_features_batch(self, index, val):
        '''
        将稀疏特征处理成 batch 的形式，后续用于线上服务推理

        Args:
            index:稀疏特征的索引
            val:稀疏特征的值

        Returns:
            batched cross feature
        '''
        batch_num = len(index)
        index = [b for a in index for b in a]
        val = [b for a in val for b in a]
        num = len(index)
        batch_size = (num - 1) // batch_num + 1

        index = [index[i * batch_size:(i + 1) * batch_size] for i in range(batch_num)]
        val = [val[i * batch_size:(i + 1) * batch_size] for i in range(batch_num)]
        for i in range(batch_num):
            if len(val[i]) == 0:
                index[i] = index[i - 1]
                val[i] = val[i - 1]
            elif len(val[i]) != batch_size:
                while len(val[i]) < batch_size:
                    index[i].append(index[i][-1])
                    val[i].append(val[i][-1])

        return index, val

    def to_tfrecord(self, csvfile, filename):
        """Extract features from the original data in csv format, and convert to tfrecord format.

        .. note::
            Tensorflow uses tensorflow.TFRecordDataloader to load tfrecord files

            Pytorch uses pytorch.TFRecordDataloader to load tfrecord files

        Args:
            csv_file (str): the file, in which original csv data is saved
            h5_file (str): the file, to which tfrecord data will save

        Returns:

        """
        writer = tf.python_io.TFRecordWriter(filename)
        data = open(csvfile, 'r', encoding='utf8').read().split('\n')[1:-1]
        role_id_hashs, sequence_ids, sequence_times, sequence_time_gapss, cross_features_indexs, cross_features_vals, user_features_ids, \
        pos_labels, neg_labels, masks, cur_times = self.feature_extraction(data)
        print('feature_extraction')
        for i in range(len(data)):
            role_id_hash = role_id_hashs[i]
            sequence_id = sequence_ids[i]
            sequence_time = sequence_times[i]
            sequence_time_gaps = sequence_time_gapss[i]
            cross_features_index = cross_features_indexs[i]
            cross_features_val = cross_features_vals[i]
            user_features_id = user_features_ids[i]
            pos_label = pos_labels[i]
            neg_label = neg_labels[i]
            mask = masks[i]
            cur_time = cur_times[i]

            sequence_id_feature = [tf.train.Feature(int64_list=tf.train.Int64List(value=sequence_id[i])) for i in range(self.seq_num)]
            sequence_time_feature = [tf.train.Feature(int64_list=tf.train.Int64List(value=sequence_time[i])) for i in range(self.seq_num)]
            sequence_time_gaps_feature = [tf.train.Feature(int64_list=tf.train.Int64List(value=sequence_time_gaps[i])) for i in range(self.seq_num)]

            role_id_hash_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=[role_id_hash]))
            cross_features_index_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=cross_features_index))
            cross_features_val_feature = tf.train.Feature(float_list=tf.train.FloatList(value=cross_features_val))
            user_features_id_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=user_features_id))
            pos_label_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=pos_label))
            neg_label_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=neg_label))
            mask_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=mask))
            cur_time_feature = tf.train.Feature(int64_list=tf.train.Int64List(value=[cur_time]))

            feature = {
                # 'hist_num': hist_num_feature,
                'role_id_hash': role_id_hash_feature,
                "cross_features_index": cross_features_index_feature,
                "cross_features_val": cross_features_val_feature,
                "user_features_id": user_features_id_feature,
                "pos_label": pos_label_feature,
                "neg_label": neg_label_feature,
                'mask': mask_feature,
                'cur_time': cur_time_feature,
            }
            for seq_num_i in range(self.seq_num):
                feature['sequence_id_' + str(seq_num_i)] = sequence_id_feature[seq_num_i]
                feature['sequence_time_' + str(seq_num_i)] = sequence_time_feature[seq_num_i]
                feature['sequence_time_gaps_' + str(seq_num_i)] = sequence_time_gaps_feature[seq_num_i]

            seq_example = tf.train.Example(
                features=tf.train.Features(feature=feature)
            )
            writer.write(seq_example.SerializeToString())
        writer.close()

    def read_tfrecord(self, filename, is_pred=False):
        '''
        加载 tfrecord 数据，并完成训练数据集的构造。
        包括序列特征构建、ID特征构建、稀疏特征构建、标签构建等

        Args:
            filename: 文件名；
            is_pred: 是否是预测阶段。

        Returns:
            TFRecordDataLoader
        '''

        def _parse_exmp(serial_exmp):
            context_features = {
                "role_id_hash": tf.io.FixedLenFeature([], dtype=tf.int64),
                "cross_features_index": tf.io.VarLenFeature(dtype=tf.int64),
                "cross_features_val": tf.io.VarLenFeature(dtype=tf.float32),
                "user_features_id": tf.io.VarLenFeature(dtype=tf.int64),
                # "label_week_id": tf.io.VarLenFeature(dtype=tf.int64),
                "pos_label": tf.io.VarLenFeature(dtype=tf.int64),
                "neg_label": tf.io.VarLenFeature(dtype=tf.int64),
                "mask": tf.io.VarLenFeature(dtype=tf.int64),
                "cur_time": tf.io.FixedLenFeature([], dtype=tf.int64),
            }

            for seq_num_i in range(self.seq_num):
                context_features['sequence_id_' + str(seq_num_i)] = tf.io.VarLenFeature(dtype=tf.int64)
                context_features['sequence_time_' + str(seq_num_i)] = tf.io.VarLenFeature(dtype=tf.int64)
                context_features['sequence_time_gaps_' + str(seq_num_i)] = tf.io.VarLenFeature(dtype=tf.int64)

            context_parsed = tf.io.parse_single_example(serialized=serial_exmp, features=context_features)

            sequence_id = [tf.sparse_to_dense(context_parsed['sequence_id_' + str(i)].indices, [self.maxlen],
                                              context_parsed['sequence_id_' + str(i)].values) for i in range(self.seq_num)]
            sequence_time = [tf.sparse_to_dense(context_parsed['sequence_time_' + str(i)].indices, [self.maxlen],
                                                context_parsed['sequence_time_' + str(i)].values) for i in range(self.seq_num)]
            sequence_time_gaps = [tf.sparse_to_dense(context_parsed['sequence_time_gaps_' + str(i)].indices, [self.maxlen],
                                                     context_parsed['sequence_time_gaps_' + str(i)].values)
                                  for i in range(self.seq_num)]
            role_id_hash = context_parsed['role_id_hash']
            cross_features_index = tf.sparse.to_dense(context_parsed['cross_features_index'])
            cross_features_val = tf.sparse.to_dense(context_parsed['cross_features_val'])
            cross_feature = tf.SparseTensor(values=cross_features_val, indices=tf.expand_dims(cross_features_index, -1),
                                            dense_shape=[self.cross_feature_num])
            user_feature = tf.sparse.to_dense(context_parsed['user_features_id'])

            pos_label = tf.sparse.to_dense(context_parsed['pos_label'])
            neg_label = tf.sparse.to_dense(context_parsed['neg_label'])
            mask = tf.sparse.to_dense(context_parsed['mask'])
            cur_time = context_parsed['cur_time']

            indices = tf.expand_dims(pos_label, -1)
            updates = tf.ones_like(pos_label)
            shape = tf.constant([self.output_unit], dtype='int64')
            label = tf.scatter_nd(indices, updates, shape)

            if self.multi_class and self.neg_sample:
                indices = tf.expand_dims(mask, -1)
                updates = tf.ones_like(mask)
                shape = tf.constant([self.output_unit], dtype='int64')
                mask = tf.scatter_nd(indices, updates, shape)

            else:
                if self.output_unit > 1:
                    mask = tf.ones([self.output_unit])
                else:
                    mask = tf.ones([1])
            return role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_feature, user_feature, mask, cur_time, label

        def _flat_map_fn(role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_feature, user_feature, mask, cur_time, label):

            return dataset_ops.Dataset.zip((
                role_id_hash.batch(batch_size=self.batchsize),
                sequence_id.padded_batch(self.batchsize, padded_shapes=([self.seq_num, self.maxlen])),
                sequence_time.padded_batch(self.batchsize, padded_shapes=([self.seq_num, self.maxlen])),
                sequence_time_gaps.padded_batch(self.batchsize, padded_shapes=([self.seq_num, self.maxlen])),
                cross_feature.batch(batch_size=self.batchsize),
                user_feature.padded_batch(self.batchsize, padded_shapes=([self.user_feature_num])),
                mask.batch(batch_size=self.batchsize),
                cur_time.batch(batch_size=self.batchsize),
                label.batch(batch_size=self.batchsize),
            ))

        def preprocess_fn(a, b, c, d, e, f, g, h, i):
            '''A transformation function to preprocess raw data
            into trainable input. '''
            return (a, b, c, d, e, f, g, h), i
            # return (a, b, c, d, e, f, g, i), tf.one_hot(h, self.output_unit) if self.output_unit > 1 else h

        # tf.enable_eager_execution()
        dataset = tf.data.TFRecordDataset(filename, num_parallel_reads=4)
        if is_pred:
            dataset_train = dataset \
                .map(_parse_exmp, num_parallel_calls=1) \
                .window(size=self.batchsize, drop_remainder=False) \
                .flat_map(_flat_map_fn) \
                .map(preprocess_fn)
        else:
            dataset_train = dataset \
                .map(_parse_exmp, num_parallel_calls=4) \
                .shuffle(10000) \
                .window(size=self.batchsize, drop_remainder=True) \
                .flat_map(_flat_map_fn) \
                .map(preprocess_fn) \
                .repeat()
        # print(dataset_train.make_one_shot_iterator().get_next())
        return dataset_train

    def to_hdf5(self, csv_file, h5_file):
        """Extract features from the original data in csv format, and convert to hdf5 format.

        .. note::
            Tensorflow uses tensorflow.HDF5Dataloader to load hdf5 files

            Pytorch uses pytorch.HDF5Dataloader to load hdf5 files

        Args:
            csv_file (str): the file, in which original csv data is saved
            h5_file (str): the file, to which hdf5 data will save

        Returns:

        """
        with open(csv_file, 'r', encoding='utf8') as iin:
            data = iin.read().split('\n')[1:-1]
            role_id_hash, sequence_id, sequence_time, sequence_time_gaps, cross_features_index, cross_features_val, user_features_id, \
            cur_time, pos_label = self.feature_extraction(data, h5=True)

        import h5py
        with h5py.File(h5_file, 'w') as f:
            f.create_dataset('role_id_hash', data=np.array(role_id_hash))
            f.create_dataset('sequence_id', data=np.array(sequence_id))
            f.create_dataset('sequence_time', data=np.array(sequence_time))
            f.create_dataset('sequence_time_gaps', data=np.array(sequence_time_gaps))
            if len(set(len(x) for x in cross_features_index)) == 1:
                f.create_dataset('cross_features_index', data=cross_features_index)
                f.create_dataset('cross_features_val', data=cross_features_val)
            else:
                f.create_dataset('cross_features_index', data=cross_features_index, dtype=h5py.special_dtype(vlen=np.dtype('int64')))
                f.create_dataset('cross_features_val', data=cross_features_val, dtype=h5py.special_dtype(vlen=np.dtype('float32')))
            f.create_dataset('user_features_id', data=np.array(user_features_id))
            f.create_dataset('cur_time', data=np.array(cur_time))
            f.create_dataset('pos_label', data=np.array(pos_label))


if __name__ == '__main__':
    a = tf.constant([[0, 0, 0, 0],[0, 0, 1, 2]],dtype=tf.float32)
    idx = tf.where(a > 0)
    output = tf.gather_nd(a, idx)
    output = tf.reshape(output,[2,1])
    output2 = tf.layers.Dense(10)(output)
    with tf.Session() as sess:
        res1 = sess.run(idx)
        res2 = sess.run(output)
        print(res1)
        print(res2)
