#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import codecs
import argparse

class Entity:
    def __init__(self):
        self.lbl_idxs=[]

    def addIdx(self,idx):
        self.lbl_idxs.append(idx)

    def clear(self):
        self.lbl_idxs=[]

class Sentence:
    def __init__(self):
        self.tokens=[]
        self.labels=[]
        self.whole_tokens=[]
        self.whole_labels=[]
        self.rec_tokens=[]
        self.rec_labels=[]

    def addToken(self,token,label):
        self.tokens.append(token)
        self.labels.append(label)

    def clear(self):
        self.tokens=[]
        self.labels=[]
        self.whole_tokens=[]
        self.whole_labels=[]
        self.rec_tokens=[]
        self.rec_labels=[]

    def simplif(self):
        for w,lbl in zip(self.whole_tokens,self.whole_labels):
            if lbl=='Nr' or lbl=='Ns' or lbl=='Nt':
                self.rec_tokens.append(w)
                self.rec_labels.append(lbl)

    def generate_whole(self):
        nr=Entity()
        name=""
        ns=Entity()
        loc=""
        nt=Entity()
        organ=""
        for idx,lbl in enumerate(self.labels):
            #print(idx,lbl)
            if lbl=='B-Nr':
                nr.clear()
                nr.addIdx(idx)
                #print(nr.lbl_idxs)
            if lbl=='I-Nr':
                nr.addIdx(idx)
            if lbl=='E-Nr':
                nr.addIdx(idx)
                #print(nr.lbl_idxs)
                nn=len(nr.lbl_idxs)
                if nr.lbl_idxs[-1]-nr.lbl_idxs[0]==nn-1:
                    # recognition true
                    begin=nr.lbl_idxs[0]
                    end=nr.lbl_idxs[-1]
                    for i in range(begin,end+1):
                        name+=self.tokens[i]
                    #print("name:",name)
                    self.whole_tokens.append(name)
                    self.whole_labels.append('Nr')
                    nr.clear()
                    name=""
            if lbl=='S-Nr':
                self.whole_tokens.append(self.tokens[idx])
                self.whole_labels.append('Nr')
                nr.clear()
                name=""

            if lbl=='B-Ns':
                ns.clear()
                ns.addIdx(idx)
            if lbl=='I-Ns':
                ns.addIdx(idx)
            if lbl=='E-Ns':
                ns.addIdx(idx)
                nn=len(ns.lbl_idxs)
                if ns.lbl_idxs[-1]-ns.lbl_idxs[0]==nn-1:
                    # recognition true
                    begin=ns.lbl_idxs[0]
                    end=ns.lbl_idxs[-1]
                    for i in range(begin,end+1):
                        loc+=self.tokens[i]
                    #print("name:",name)
                    self.whole_tokens.append(loc)
                    self.whole_labels.append('Ns')
                    ns.clear()
                    loc=""
            if lbl=='S-Ns':
                self.whole_tokens.append(self.tokens[idx])
                self.whole_labels.append('Ns')
                ns.clear()
                loc=""

            if lbl=='B-Nt':
                nt.clear()
                nt.addIdx(idx)
            if lbl=='I-Nt':
                nt.addIdx(idx)
            if lbl=='E-Nt':
                nt.addIdx(idx)
                nn=len(nt.lbl_idxs)
                if nt.lbl_idxs[-1]-nt.lbl_idxs[0]==nn-1:
                    # recognition true
                    begin=nt.lbl_idxs[0]
                    end=nt.lbl_idxs[-1]
                    for i in range(begin,end+1):
                        organ+=self.tokens[i]
                    self.whole_tokens.append(organ)
                    self.whole_labels.append('Nt')
                    nt.clear()
                    organ=""
            if lbl=='S-Nt':
                self.whole_tokens.append(self.tokens[idx])
                self.whole_labels.append('Nt')
                nt.clear()
                organ=""

            if lbl=='O':
                self.whole_tokens.append(self.tokens[idx])
                self.whole_labels.append(lbl)
                nr.clear()
                ns.clear()
                nt.clear()
                name=""
                loc=""
                organ=""
                    
                
                

def calcF(std_cnt,model_cnt,correct_cnt):
    if std_cnt==0 or model_cnt==0:
        return 0,0,0
    precision=correct_cnt/float(model_cnt)
    recall=correct_cnt/float(std_cnt)
    fscore=2*precision*recall/(precision+recall)
    return precision,recall,fscore

def evaluate(correct_output_path,model_output_path,correct_mtag_name,model_mtag_name):
    std_cnt_dict={'B-Nr':0,'I-Nr':0,'E-Nr':0,'S-Nr':0,'B-Ns':0,'I-Ns':0,'E-Ns':0,'S-Ns':0,'B-Nt':0,'I-Nt':0,'E-Nt':0,'S-Nt':0}
    usr_cnt_dict={'B-Nr':0,'I-Nr':0,'E-Nr':0,'S-Nr':0,'B-Ns':0,'I-Ns':0,'E-Ns':0,'S-Ns':0,'B-Nt':0,'I-Nt':0,'E-Nt':0,'S-Nt':0}
    usrcrt_cnt_dict={'B-Nr':0,'I-Nr':0,'E-Nr':0,'S-Nr':0,'B-Ns':0,'I-Ns':0,'E-Ns':0,'S-Ns':0,'B-Nt':0,'I-Nt':0,'E-Nt':0,'S-Nt':0}
    std_whole_dict={'Nr':0,'Ns':0,'Nt':0}
    usr_whole_dict={'Nr':0,'Ns':0,'Nt':0}
    usrcrt_whole_dict={'Nr':0,'Ns':0,'Nt':0}
    whole_list=['Nr','Ns','Nt']
    tag_list=['B-Nr','I-Nr','E-Nr','S-Nr','B-Ns','I-Ns','E-Ns','S-Ns','B-Nt','I-Nt','E-Nt','S-Nt']

    correct_tagf=codecs.open(correct_mtag_name,"w+",encoding="utf-8")
    model_tagf=codecs.open(model_mtag_name,"w+",encoding="utf-8")

    with codecs.open(correct_output_path,"r",encoding="utf-8") as fcrt:
        with codecs.open(model_output_path,"r",encoding="utf-8") as fmdl:
            for stdline,usrline in zip(fcrt,fmdl):
                stdline=stdline.strip()
                stdsentence=Sentence()
                for token in stdline.split():
                    stdsentence.addToken(token.split('/')[0],token.split('/')[-1])
                usrline=usrline.strip()
                usrsentence=Sentence()
                for token in usrline.split():
                    usrsentence.addToken(token.split('/')[0],token.split('/')[-1])
                for stdtag,usrtag in zip(stdsentence.labels,usrsentence.labels):
                    if stdtag in std_cnt_dict:
                        std_cnt_dict[stdtag]+=1
                        if stdtag ==usrtag:
                            usrcrt_cnt_dict[usrtag]+=1
                    if usrtag in usr_cnt_dict:
                        usr_cnt_dict[usrtag]+=1
                stdsentence.generate_whole()
                usrsentence.generate_whole()
                std_mtag=""
                for w,lbl in zip(stdsentence.whole_tokens,stdsentence.whole_labels):
                    #print("%s/%s" % (w,lbl))
                    std_mtag+=w+"/"+lbl+" "
                std_mtag=std_mtag.strip()
                usr_mtag=""
                for w,lbl in zip(usrsentence.whole_tokens,usrsentence.whole_labels):
                    usr_mtag+=w+"/"+lbl+" "
                usr_mtag=usr_mtag.strip()
                #print("std: %s" % std_mtag)
                #print("model: %s" % usr_mtag)
                correct_tagf.write("%s\n" % std_mtag)
                model_tagf.write("%s\n" % usr_mtag)
                stdsentence.simplif()
                usrsentence.simplif()
                # this code must run first, judge op may clear list
                for lbl in usrsentence.rec_labels:
                    usr_whole_dict[lbl]+=1
                for w,lbl in zip(stdsentence.rec_tokens,stdsentence.rec_labels):
                    #print("%s/%s" % (w,lbl))
                    std_whole_dict[lbl]+=1
                    for w_,lbl_ in zip(usrsentence.rec_tokens,usrsentence.rec_labels):
                        if lbl==lbl_ and w==w_:
                            usrcrt_whole_dict[lbl]+=1
                            usrsentence.rec_tokens.remove(w_)
                            usrsentence.rec_labels.remove(lbl_)
                            break

                #print(usrcrt_whole_dict)
                
                stdsentence.clear()
                usrsentence.clear()

    correct_tagf.close()
    model_tagf.close()
    #print("std B-Nr:%d,model B-Nr:%d" % (std_cnt_dict['B-Nr'],usr_cnt_dict['B-Nr']))
    for tag in tag_list:
        p,r,f=calcF(std_cnt_dict[tag],usr_cnt_dict[tag],usrcrt_cnt_dict[tag])
        print("%s std:%d, model:%d, model correct:%d precision:%f, recall:%f, fscore:%f" % (tag,std_cnt_dict[tag],usr_cnt_dict[tag],usrcrt_cnt_dict[tag],p,r,f) )

    for tag in whole_list:
        p,r,f=calcF(std_whole_dict[tag],usr_whole_dict[tag],usrcrt_whole_dict[tag])
        print("%s std:%d, model:%d, model correct:%d precision:%f, recall:%f, fscore:%f" % (tag,std_whole_dict[tag],usr_whole_dict[tag],usrcrt_whole_dict[tag],p,r,f) )
    




def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--correct_output_path",default="correct_out.txt", type=str,help="correct output path")
    parser.add_argument("--model_output_path",default="model_out.txt",type=str,help="model output path")
    args=parser.parse_args()
    correct_output_path=args.correct_output_path
    model_output_path=args.model_output_path
    correct_mtag_name='correct_mtag.txt'
    model_mtag_name='model_mtag.txt'
    evaluate(correct_output_path,model_output_path,correct_mtag_name,model_mtag_name)



if __name__=='__main__':
    main()



















