#!/usr/bin/env python
# coding=utf-8

import codecs
import argparse
import os 
import sys 
import re

LABELS={'B-Nr':1, 'I-Nr':2, 'E-Nr':3, 'S-Nr':4, 'B-Ns':5, 'I-Ns':6, 'E-Ns':7, 'S-Ns':8, 'B-Nt':9, 'I-Nt':10, 'E-Nt':11, 'S-Nt':12, 'O':0}
_SPACE_SPLIT=re.compile(r'\s\s*')
totalLine=0
longLine=0
totalChars=0
MAX_LEN=80

class Sentence:
    def __init__(self):
        self.tokens=[]
        self.labels=[]
        self.chars=0

    def addToken(self,token,label):
        self.tokens.append(token)
        self.labels.append(label)
        self.chars+=1

    def clear(self):
        self.tokens=[]
        self.labels=[]
        self.chars=0

    def generate_line(self,x,y,vob):
        #x=[]
        #y=[]
        for w,lbl in zip(self.tokens,self.labels):
            if w in vob:
                idx=vob[w]
            else:
                idx=vob['unk']
            if lbl in LABELS:
                tag=LABELS[lbl]
            else:
                tag=0
            x.append(idx)
            y.append(tag)
        #line=""
        #for idx in x+y:
        #    line+=str(idx)+" "
        #line=line.strip()
        #return line


def initialize_vocabulary(w2v_path):
    with codecs.open(w2v_path,"r",encoding="utf-8") as f:
        line=f.readline().strip()
        ss=line.split()
        total=int(ss[0])
        dim=int(ss[1])
        print("total:%d,dim:%d" % (total,dim))
        vocab=[line.strip().split()[0] for line in f]
        vocab.append('unk')
        vocab_dict=dict( [(x,y+1) for (y,x) in enumerate(vocab)])
        # 0:padding len:unk
        return vocab_dict

def process_line(line,out,vob):
    global totalLine
    global longLine
    global totalChars

    line=line.strip()
    words_split=_SPACE_SPLIT.split(line)
    sentence=Sentence()
    for token in words_split:
        sentence.addToken(token.split('/')[0],token.split('/')[-1])
    nn=sentence.chars
    if sentence.chars>MAX_LEN:
        longLine+=1
    else:
        x=[]
        y=[]
        totalChars+=nn
        sentence.generate_line(x,y,vob)
        assert(nn==len(y))
        for j in range(nn,MAX_LEN):
            x.append(0)
            y.append(0)
        new_line=""
        for i in range(MAX_LEN):
            if i>0:
                new_line+=" "
            new_line+=str(x[i])
        for j in range(MAX_LEN):
            new_line+=" "+str(y[j])
        #print(new_line)
        out.write("%s\n" % new_line)
    sentence.clear()
    totalLine+=1

def getFilenamePath(rootdir):
    l_filename=[]
    l_filepath=[]
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            filepath=os.path.join(parent,filename)
            l_filename.append(filename)
            l_filepath.append(filepath)
    return l_filename,l_filepath


def main(argc,argv):
    parser=argparse.ArgumentParser()
    parser.add_argument("--word2vec_path",default="word_vectrain_50.txt",type=str,help="word2vec_path")
    parser.add_argument("--data_path",default="data",type=str,help="data_path")
    parser.add_argument("--output_path",default="out_ids_80.txt",type=str,help="output_path")

    args=parser.parse_args()
    w2v_path=args.word2vec_path
    vob=initialize_vocabulary(w2v_path)

    out=codecs.open(args.output_path,"w+",encoding="utf-8")
    _,filepaths=getFilenamePath(args.data_path)
    for filepath in filepaths:
        print(filepath)
        f=codecs.open(filepath,"r",encoding="utf-8")
        for line in f:
            line=line.strip()
            if not line:
                continue
            process_line(line,out,vob)
        f.close()
    out.close()
    print("total:%d, long lines:%d, chars:%d " % (totalLine,longLine,totalChars))


if __name__=='__main__':
    main(len(sys.argv),sys.argv)










