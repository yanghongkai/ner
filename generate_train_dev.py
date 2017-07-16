#!/usr/bin/env python
# coding=utf-8

import codecs
import random

def generate_dev(filepath,trainpath,devpath):
    f=codecs.open(filepath,"r",encoding="utf-8")
    train_out=codecs.open(trainpath,"w+",encoding="utf-8")
    dev_out=codecs.open(devpath,"w+",encoding="utf-8")
    test=0
    for line in f:
        line=line.strip()
        if not line:
            continue
        r=random.random()
        if r<=0.02 and test<100000:
            dev_out.write("%s\n" % line)
            test+=1
        else:
            train_out.write("%s\n" % line)


if __name__=='__main__':
    rootdir='baokan_2_ids_80.txt'
    trainpath='train_2_ids_80.txt'
    devpath='dev_2_ids_80.txt'
    generate_dev(rootdir,trainpath,devpath)






