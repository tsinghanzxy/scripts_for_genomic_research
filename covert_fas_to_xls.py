# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:56:16 2019

@author: Chris
"""
#credited:
#https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052

def fasta2excel(fasta,excel):
    #用于统计总序列文件的行数
    count = 0
    with open(fasta,'r') as f1:
        for eachline in f1:
            count += 1

    ###获取每条序列的位置
    index_list = []
    with open(fasta,'r') as f2:
        for i in range(count):
            a = f2.readline()
            if '>' in a:
                index = i
                index_list.append(i)
                
    index_list.append(count+1)##添加最后一条序列的结束位置            
    ###序列数为seq_num-1
    seq_num = len(index_list)
    
    ###将序列以键值对存放于字典中
    excel_dict = {}
    with open(fasta,'r') as f3:
        for j in range(seq_num-1):
            geneid = f3.readline().rstrip('\n').lstrip('')###去除换行符lstrip('')括号内去除>则不包含
            geneseq = []#初始化每个基因的序列
            for n in range((index_list[j]+1),index_list[j+1]):#每个id对应的序列行数
                geneseq.append(f3.readline().rstrip('\n'))
            excel_dict[geneid] = geneseq

    with open(excel,'w') as f4:
        for eachkey in excel_dict.keys():
            f4.writelines(eachkey)
            f4.write('\t')
            for each in excel_dict[eachkey]:
                f4.writelines(each)
            f4.write('\n')

    print(f'您所输入的序列文件有{count}行')
    print(f'您所输入的序列文件中包含的序列数目为{seq_num-1}')
fasta = input('请输入您需要转换的文件名(fasta格式)：')
excel = input('请输入您生成文件的文件名(.csv)格式:')
fasta2excel(fasta,excel)