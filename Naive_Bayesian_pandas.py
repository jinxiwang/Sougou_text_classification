# -*- coding: utf-8 -*-  
import os  
# import  jieba  
import nltk  
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve

## 由搜狗语料库 生成数据  
folder_path = '.\sougou_all'  
  
folder_list = os.listdir(folder_path)  
class_list = [] ##  
nClass = 0  
N = 500 #每类文件 最多取 2500 个样本 80%train 20%test  
train_set = []  
test_set = []  
all_words = {}  
import time  
process_times = [] ## 统计处理每个文件的时间  
for i in range(len(folder_list)):  
    new_folder_path = folder_path + '\\' + folder_list[i]  
    files = os.listdir(new_folder_path)  
    class_list.append(folder_list[i])  
    nClass += 1  
    j = 0  
    nFile = min([len(files), N])  
    for file in files:  
        if j > N:  
            break  
        starttime = time.clock()  
  
        fobj = open(new_folder_path+'\\'+file, 'r')  
        raw = fobj.read()  
 
        if j > 0.2 * nFile:  
            train_set.append([raw, class_list[i]])  
        else:  
            test_set.append([raw, class_list[i]])  
        j += 1  
        endtime = time.clock()  
        process_times.append(endtime-starttime)  
  
        print ("Folder ",i,"-file-",j, "all_words length = ", len(all_words.keys()),
            "process time:",(endtime-starttime))

train_set=pd.DataFrame(train_set,columns=['doc','label'])
test_set=pd.DataFrame(test_set,columns=['doc','label'])

vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(train_set.doc)
model2 = MultinomialNB()
model2.fit(features, train_set.label)
# print(features)
# features.to_csv('jjjj.csv')
# pred2 = model2.predict_proba(vectorizer.transform(test_set.doc))
print ("test accuracy:", model2.score(vectorizer.transform(test_set.doc),test_set.label))

test_set.to_csv('test_set.csv')
