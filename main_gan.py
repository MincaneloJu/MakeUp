# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import os
import glob
from imageio import imread, imsave ,imwrite

import cv2
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('--no_makeup', type=str, default=os.path.join('C:/Users/Big data/Desktop/db104_2_project/static/456.jpg'), help='path to the no_makeup image')
#args = parser.parse_args()

#def preprocess(img):
#    return (img / 255. - 0.5) * 2

#def deprocess(img):
#    return (img + 1) / 2


def make_upup(path):

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--no_makeup', type=str,default=os.path.join(path=path),help='path to the no_makeup image')
    # args = parser.parse_args()

    batch_size = 1
    img_size = 256

    no_makeup = cv2.resize(imread(str(path)), (img_size, img_size))

    preprocess_n = (no_makeup / 255. - 0.5) * 2
    X_img = np.expand_dims(preprocess_n, 0)
    makeups = glob.glob(os.path.join('C:/Users/Big data/Desktop/db104_2_project/imgs', 'C:/Users/Big data/Desktop/db104_2_project/imgs/makeup', '*.*'))
    result = np.ones((2 * img_size, (len(makeups) + 1) * img_size, 3))
    result[img_size: 2 *  img_size, :img_size] = no_makeup / 255.

    tf.reset_default_graph()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph(os.path.join('C:/Users/Big data/Desktop/db104_2_project/model', 'C:/Users/Big data/Desktop/db104_2_project/model/model.meta'))
    saver.restore(sess, tf.train.latest_checkpoint('C:/Users/Big data/Desktop/db104_2_project/model'))

    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name('X:0')
    Y = graph.get_tensor_by_name('Y:0')
    Xs = graph.get_tensor_by_name('generator/xs:0')

    for i in range(len(makeups)):
        makeup = cv2.resize(imread(makeups[i]), (img_size, img_size))
        preprocess_y = (makeup / 255. - 0.5) * 2
        Y_img = np.expand_dims(preprocess_y, 0)
        Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
        xx = (Xs_ + 1) / 2
        Xs_ = xx
        result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup / 255.
        result[img_size: 2 * img_size, (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]


    imsave('C:/Users/Big data/Desktop/db104_2_project/static/result.jpg', result)
#img_uint8 = result.astype(np.uint8)
#imwrite('result.jpg', img_uint8)