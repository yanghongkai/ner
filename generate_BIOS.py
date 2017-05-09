#!/usr/bin/env python
# coding=utf-8

import codecs

class Sentence:
    def __init__(self):
        self.tokens=[]
        self.labels=[]

    def addToken(self,token,label):
        self.tokens.append(token)
        self.labels.append(label)

    def clear(self):
        self.tokens=[]
        self.labels=[]

    def generate_line(self):
        x=[]
        y=[]
        for w,lbl in zip(self.tokens,self.labels):
            if lbl=="nr":
                words=w.split('_')
                nn=len(words)
                if nn>1:
                    for i in range(nn):
                        x.append(words[i])
                        if i==0:
                            y.append('B-Nr')
                        elif i==(nn-1):
                            y.append('E-Nr')
                        else:
                            y.append('I-Nr')
                else:
                    y.append('S-Nr')
                    x.append(w)
            elif lbl=="ns":
                words=w.split('_')
                nn=len(words)
                if nn>1:
                    for i in range(nn):
                        x.append(words[i])
                        if i==0:
                            y.append('B-Ns')
                        elif i==(nn-1):
                            y.append('E-Ns')
                        else:
                            y.append('I-Ns')
                else:
                    y.append('S-Ns')
                    x.append(w)
            elif lbl=="nt":
                words=w.split('_')
                nn=len(words)
                if nn>1:
                    for i in range(nn):
                        x.append(words[i])
                        if i==0:
                            y.append('B-Nt')
                        elif i==(nn-1):
                            y.append('E-Nt')
                        else:
                            y.append('I-Nt')
                else:
                    y.append('S-Nt')
                    x.append(w)
            else:
                y.append(lbl)
                x.append(w)

        line=""
        for w,lbl in zip(x,y):
            line+=w+"/"+lbl+" "
        line=line.strip()
        return line

def deal_sentence(line,out):
    sentence=Sentence()
    for token in line.split():
        sentence.addToken(token.split('/')[0],token.split('/')[-1])
    line=sentence.generate_line()
    out.write("%s\n" % line)
    sentence.clear()

def deal_file(filepath,outname):
    f=codecs.open(filepath,"r",encoding="utf-8")
    out=codecs.open(outname,"w+",encoding="utf-8")
    for line in f:
        line=line.strip()
        if not line:
            continue
        deal_sentence(line,out)

    f.close()
    out.close()

if __name__=='__main__':
    rootdir="199801_BIOS_sentence.txt"
    outname="199801_BIOS_std.txt"
    deal_file(rootdir,outname)










