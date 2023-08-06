import os
import tensorflow as tf
import numpy as np

# todo: test ocrdataloader


class SegmentationDataLoader():
    r""" Loads the ``tf.data.Dataset`` for ``PageExtraction``,``ImageExtraction``,``LayoutExtraction`` and ``BaselineDetection`` classes.

    Args:
        path (str)       : Path of the folder containing images folder and labels folder to be loaded in dataset.Folder names must be as mentioned.
        n_classes (int)  : number of classes in label images.

    """

    def __init__(self, path, n_classes):

        images_path = os.path.join(path, "images")
        labels_path = os.path.join(path, "labels")

        img_paths, label_paths = self._read_img_paths_and_labels(
            images_path,
            labels_path)
        self.n_classes = n_classes
        self.size = len(img_paths)

        ds = tf.data.Dataset.from_tensor_slices((img_paths, label_paths))
        ds = ds.map(self._decode_and_resize)
        ds = ds.apply(tf.data.experimental.ignore_errors())

        self.dataset = ds

    def _decode_and_resize(self, image_filename, label_filename):
        r""" Reads images. Reads and one hot encodes labels.

        Args:
            image_filename (str) : Path of image file.
            label_filename (str) : Path of label file.

        Returns:
            image (tf.Tensor)  : Image tensor.
            label (tf.Tensor)  : Label tensor.
        """
        image = tf.io.read_file(image_filename)
        image = tf.io.decode_png(image, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        resize = (tf.shape(image[:, :, 0])//32)*32
        image = tf.image.resize(image, resize)
        label = tf.io.read_file(label_filename)
        label = tf.io.decode_png(label, channels=3)
        label = tf.image.resize(label, resize)
        label = tf.cast((label[:, :, 0] > 100), tf.int32)
        label = tf.one_hot(label, self.n_classes)
        return image, label

    def __call__(self, batch_size=1, repeat=1):
        r"""

        Args:
            batch_size (int,optional) : Batchsize of ``tf.data.datset``. Default value 1.
            repeat (int, optional)    : Specifies the number of times the dataset can be iterated.Default value 1.


        Return:
            ds (tf.data.dataset)  : Dataloader.
        """
        ds = self.dataset
        ds = ds.batch(batch_size).repeat(repeat)
        ds = ds.prefetch(tf.data.experimental.AUTOTUNE)
        return ds

    def __len__(self):
        r"""
        Return:
            lenght of dataset
        """
        return self.size

    def _read_img_paths_and_labels(self, images_path, labels_path):
        r"""Reads paths of images and labels.


        Args:
            images_path (str) : Path of the folder of images.
            labels_path (str) : Path of the folder of labels.

        Returns:
            img_path (list)   : List of image paths.
            label_path (list) : List of label paths.

        """
        img_path = os.listdir(images_path)
        img_path.sort()
        img_path = [str(os.path.join(images_path, i)) for i in img_path]
        label_path = os.listdir(labels_path)
        label_path.sort()
        label_path = [str(os.path.join(labels_path, i)) for i in label_path]

        return img_path, label_path


class OCRDataLoader():
    r""" Loads the ``tf.data.Dataset`` for ``OCR`` class.

    Args:
        path (strs)        :  Path of  folder containing images folder,labels.txt and table.txt to be loaded in dataset.Name of folders and files should be same as mentioned.
    """

    def __init__(self, path, height):

        images_path = os.path.join(path, "images")
        labels_path = os.path.join(path, "labels.txt")
        table_path = os.path.join(path, "table.txt")
        img_paths, labels = self._read_img_paths_and_labels(
            images_path,
            labels_path)
        self.size = len(img_paths)
        self.path = path
        self.height = height

        with open(table_path) as f:
            self.inv_table = [char.strip() for char in f]
        self.n_classes = len(self.inv_table)
        self.blank_index = self.n_classes - 1

        self.table = tf.lookup.StaticHashTable(tf.lookup.TextFileInitializer(
            table_path, tf.string, tf.lookup.TextFileIndex.WHOLE_LINE,
            tf.int64, tf.lookup.TextFileIndex.LINE_NUMBER), self.blank_index)

        ds = tf.data.Dataset.from_tensor_slices((img_paths, labels))
        ds = ds.map(self._decode_and_resize)
        ds = ds.apply(tf.data.experimental.ignore_errors())

        self.dataset = ds

    def _decode_and_resize(self, filename, label):
        r""" Reads image.

        Args:
            filename (str) : Name of file.
            label    (str) : Label of  image.

        Returns:
            image  (tf.Tensor) : Image Tensor
            labels (tf.Tensor):  Label tensor

        """
        image = tf.io.read_file(filename)
        image = tf.io.decode_png(image, channels=1)
        image = 1.0-tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize(
            image, (self.height, tf.shape(image)[-2]), preserve_aspect_ratio=True)
        return image, label

    def _convert_label(self, image, label):
        r""" Maps chars in label to integers  according to table.txt

        Args:
            image (tf.tensor) : Image tensor
            label  (str)      : label

        Returns:
            image (tf.Tensor) : Image tensor. 
            label (tf.Tensor) : Label sparse tensor.
        """
        chars = tf.strings.unicode_split(label, input_encoding="UTF-8")
        mapped_label = tf.ragged.map_flat_values(self.table.lookup, chars)
        sparse_label = mapped_label.to_sparse()
        label = tf.cast(sparse_label, tf.int32)
        return image, label

    def __len__(self):
        return self.size

    def __call__(self, batch_size=8, repeat=1):
        r"""
        Returns:
            ds (tf.data.dataset) : Dataloader.
            """
        ds = self.dataset
        ds = ds.batch(batch_size).map(
            self._convert_label).repeat(repeat)
        ds = ds.prefetch(tf.data.experimental.AUTOTUNE)
        return ds

    def _read_img_paths_and_labels(self, images_path, labels_path):
        r"""reads filenames and respective labels.

        Args:
            imgages_path (str)  : Path of image folder.
            labels_path (str)  : path of label.txt
        Returns:
            img_path (list)   : List of  images filenames.
            label (list)      : List of labels.
        """
        img_path_ = os.listdir(images_path)
        img_path = [os.path.join(images_path, i) for i in img_path_]

        label_ = open(labels_path, 'r')
        labels_ = label_.readlines()
        labels_ = [labels_[i].split(":")[1].strip()
                   for i in range(len(labels_))]
        labels = []
        for i in img_path:
            labels.append(labels_[int(i.split(".")[0].split("/")[-1])])
        return img_path, labels

    def map2string(self, inputs):
        strings = []
        for i in inputs:
            text = [self.inv_table[char_index] for char_index in i
                    if char_index != self.blank_index]
            strings.append(''.join(text))
        return strings

    def decode(self, inputs, from_pred=True, method='beam_search', merge_repeated=True):
        self.merge_repeated = merge_repeated
        if from_pred:
            logit_length = tf.fill([tf.shape(inputs)[0]], tf.shape(inputs)[1])
            if method == 'greedy':
                decoded, _ = tf.nn.ctc_greedy_decoder(
                    inputs=tf.transpose(inputs, perm=[1, 0, 2]),
                    sequence_length=logit_length,
                    merge_repeated=self.merge_repeated)
            elif method == 'beam_search':
                decoded, _ = tf.nn.ctc_beam_search_decoder(
                    inputs=tf.transpose(inputs, perm=[1, 0, 2]),
                    sequence_length=logit_length)
            inputs = decoded[0]
        decoded = tf.sparse.to_dense(inputs,
                                     default_value=self.blank_index).numpy()
        decoded = self.map2string(decoded)
        return decoded
