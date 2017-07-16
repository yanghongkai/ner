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
                    
                
                


def process_tag(filepath,outname):
    
    out=codecs.open(outname,"w+",encoding="utf-8")
    with codecs.open(filepath,"r",encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            sentence=Sentence()
            if not line:
                continue
            for token in line.split():
                sentence.addToken(token.split('/')[0],token.split('/')[-1])
            sentence.generate_whole()
            newline=""
            for w,lbl in zip(sentence.whole_tokens,sentence.whole_labels):
                newline+=w+"/"+lbl+" "
            newline=newline.strip()
            sentence.clear()
            out.write("%s\n" % newline)
    out.close()

   
    




def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--file_path",default="correct_out.txt", type=str,help="correct output path")
    parser.add_argument("--out_path",default="model_out.txt",type=str,help="model output path")
    args=parser.parse_args()
    filepath=args.file_path
    outpath=args.out_path
    process_tag(filepath,outpath)



if __name__=='__main__':
    main()



















