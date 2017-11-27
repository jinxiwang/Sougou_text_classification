#! /usr/bin/env Python3
# -*- encoding:utf-8 -*-  
import os
from xml.dom import minidom  
from urllib.parse import urlparse

def file_fill(file_dir):
    for root, dirs, files in os.walk(file_dir):      #扫描该目录下的文件夹和文件，返回根目录路径，文件夹列表，文件列表
        print(root)
        print(dirs)
        print(files)
        for f in files:
            tmp_dir = '.\sougou_after2' + '\\' + f  # 加上标签后的文本  
            text_init_dir = file_dir + '\\' + f     #原始文本  
            print(text_init_dir)
            print(tmp_dir)
            file_source = open(text_init_dir, 'r', encoding='ansi') #打开文件，并将字符按照utf-8编码，返回unicode字节流
            print(file_source)
            ok_file = open(tmp_dir, 'a+', encoding='utf-8')  
            start = '<docs>\n'  
            end = '</docs>'  
            line_content = file_source.readlines()  #按行读取
            print(line_content)
            ok_file.write(start)  
            for lines in line_content:  
                text_temp = lines.replace('&', '.')    #替换：replace(old,new,[max]) max最多替换的次数
                text = text_temp.replace('', '')
                ok_file.write(text)  
            ok_file.write('\n' + end)  
  
            file_source.close()  
            ok_file.close()
    print('finished!')

def file_read(file_dir):
    #建立url和类别的映射词典,可以参考搜狗实验室的对照.txt,有17类，这里增加了奥运，减少了社会、国内和国际新闻、招聘
    # dicurl = {'auto.sohu.com':'qiche','it.sohu.com':'hulianwang','health.sohu.com':'jiankang','sports.sohu.com':'tiyu',
    # 'travel.sohu.com':'lvyou','learning.sohu.com':'jiaoyu','career.sohu.com':'zhaopin','cul.sohu.com':'wenhua',
    # 'mil.news.sohu.com':'junshi','house.sohu.com':'fangchan','yule.sohu.com':'yule','women.sohu.com':'shishang',
    # 'media.sohu.com':'chuanmei','gongyi.sohu.com':'gongyi','2008.sohu.com':'aoyun', 'business.sohu.com': 'shangye'} 
    dicurl = {'auto.sohu.com':'qiche','it.sohu.com':'hulianwang','health.sohu.com':'jiankang','sports.sohu.com':'tiyu',
                'travel.sohu.com':'lvyou','learning.sohu.com':'jiaoyu','cul.sohu.com':'wenhua',
                'mil.news.sohu.com':'junshi','house.sohu.com':'fangchan','yule.sohu.com':'yule','women.sohu.com':'shishang',
                'media.sohu.com':'chuanmei','gongyi.sohu.com':'gongyi','2008.sohu.com':'aoyun', 'business.sohu.com': 'shangye'} 
    path = ".\sougou_all\\"     
    for root, dirs, files in os.walk(file_dir):  
        for f in files:
            print(f)
            doc = minidom.parse(file_dir + "\\" + f)  
            root = doc.documentElement  
            claimtext = root.getElementsByTagName("content")  
            claimurl = root.getElementsByTagName("url")  
            for index in range(0, len(claimurl)):  
                if (claimtext[index].firstChild == None):  
                    continue  
                url = urlparse(claimurl[index].firstChild.data)  
                if url.hostname in dicurl:  
                    if not os.path.exists(path + dicurl[url.hostname]):  
                        os.makedirs(path + dicurl[url.hostname])  
                    fp_in = open(path + dicurl[url.hostname] + "\%d.txt" % (len(os.listdir(path + dicurl[url.hostname])) + 1),"w")  
                    temp_bytescontent = (claimtext[index].firstChild.data).encode('GBK','ignore')   #这里的ignore是说，如果编码过程中有GBK不认识的字符可以忽略
                    fp_in.write(temp_bytescontent.decode('GBK','ignore'))
    print('finished!')

def test():
    file_fill('.\sougou_before2')
    # file_fill('.\text2')

    file_read(".\sougou_after2")

if __name__=="__main__":   
  
    test()