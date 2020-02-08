# !wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.zh.300.bin.gz
# !gunzip cc.zh.300.bin.gz

import pandas as pd
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models.keyedvectors import KeyedVectors
import time
import random
from pymongo import MongoClient

from gensim.models.fasttext import FastText
# model = FastText.load_fasttext_format('E:/db104_2_project/model/cc.zh.300.bin')

def env_search(userstr):
    # return print("這個就是有跑道 env_search裡面喔!!! 真的在分析了" ,userstr)
    word = pd.read_excel('E:/db104_2_project/all.xlsx')
    url = word['網址']
    word1 = word["內文"]
    title = word["標題"]
    dict_1 = ["約會", "上課", "上班", "旅遊", "聚會", "出門", "霧眉"]
    dict_2 = ["韓系", "日系", "歐美", "眼妝", "口紅", "修容", "全妝", "唇膏", "淡妝", "濃妝", "妝容"]
    Index_1 = []  # 第一層相關字的index
    str_1 = ""  # 第一層相關字
    Index_2 = []  # 第二層相關字的index
    str_2 = ""  # 第二層相關字
    Index_3 = []  # 所得的結果
    # 第一層
    for i in dict_1:
        if i in userstr:
            str_1 = i
            for n, article in enumerate(word1):
                if str_1 in str(article):
                    Index_1.append(n)
            else:
                break
    # 第二層
    for i in dict_2:
        if i in userstr:
            str_2 = i
            for s in Index_1:
                if str_2 in str(word1[s]):
                    Index_2.append(s)
            else:
                break
    if Index_2:
        Index_3 = Index_2
    else:
        Index_3 = Index_1

    if Index_3:
        Index_3 = Index_3

    else:

        result = "無相關資料"
        return result

    # 利用work2vec比對詞向量
    score = []
    seg = []  # 文章的index和詞向量分數
    if str_2:
        str_2 = str_2
    else:
        str_2 = "妝"
    text1 = str_1 + str_2
    print("text1: ", text1)
    print("Index3 : ", Index_3)
    print("title:", title)

    # for i in Index_3:
    #     try:
    #         similar = model.wv.wmdistance(text1, title[i])
    #         print("similar ; " ,similar)
    #         com = (i, similar, title[i])
    #         seg.append(com)
    #         score.append(similar)
    #     except:
    #         pass
    # print("seg :", seg)
    for i in Index_3:
        try:
            word_vectors = KeyedVectors.load_word2vec_format("E:/db104_2_project/model_env/makeup.model%s.bin" % (i) ,binary=True)

            similar = word_vectors.similarity(str_1, str_2)
            # print("這是 similar 第 %s : " % (i), similar)
            # print(i, gogo + "," + str(like1))
            com = (i, similar)
            seg.append(com)
            score.append(similar)
        except:
            pass
    # print("seg : " ,seg)
    # print("score : " ,score)


    # 排序文章分數
    sort_score = []
    ans = sorted(score, reverse=True)
    for i in ans:
        if i not in sort_score:
            sort_score.append(i)
    # 選出最高三則貼文
    hightest = []
    for n in range(0, len(seg)):
        for y in sort_score[0:5]:
            if seg[n][1] == y:
                hightest.append(seg[n][0])
    print("第一階段 : " ,hightest)
    if len(hightest) > 3:
        final = random.sample(hightest, 3)
        print("第二階段 : " ,final)
    elif len(hightest) == 0:
        # hightest = "無相關資料"
        return 0
    else:
        final = hightest

    print("Index結果 : ", final)
    # final = [1089 ,4226 ,1178]
    # return final
    #連接mongo提取文章資料
    mongo_client = MongoClient('mongodb://10.120.38.27:15000/')
    db = mongo_client.env_search
    push = []
    for i in final:
        push_inside = []
        tag_ = str_1 + "x" + str_2
        push_inside.append(tag_)
        a = db.env_search.find({'_id': i})
        xx = ""
        for x in a:
            xx = x
        for key, value in xx.items():
            if key == "標題" or key == "網址":
                push_inside.append(value)
        push.append(push_inside)
    if push:
        return push
    else:
        push = "無相關資料"
        return 0



