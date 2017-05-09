#!/usr/bin/env python
# coding=utf-8

import codecs
import re

def deal_sentence(line,out):
    #print(line)
    m=re.match(r'^\d+-\d+-\d+-\d+/m\s+(.*)',line)
    #print(m.groups())
    #print(m.group(1))
    tokens=re.split(r'[\s]\s*',m.group(1))
    #print(tokens)
    BEGIN=False
    new_line=""
    for token in tokens:
        #print(token)
        if(re.search(r'\[',token)):
           BEGIN=True
           new_token=""
           #print(token)
           token=token.split('[')[-1]
           #new_token+=token.split('/')[0]
        if(re.search(r'\]',token)):
           #print(token)
           BEGIN=False
           new_token+=token.split(']')[0].split('/')[0]
           new_token+="/"+token.split(']')[-1]
           #print(new_token)
           new_line+=" "+new_token
        if BEGIN:
            new_token+=token.split('/')[0]+"_"
        else:
            if not re.search(r'\]',token):
                #print(token)
                new_line+=" "+token
    new_line=new_line.strip()
    #print(new_line)
    tokens=new_line.split()
    new_line=""
    SURNAME=False
    for idx,token in enumerate(tokens):
        w=token.split("/")[0]
        pos=token.split("/")[-1]
        if pos!="nr":
            new_line+=w+"/"+pos+" "
        if idx+1>=len(tokens):
            nextpos="w" #pad no use
        else:
            nextpos=tokens[idx+1].split("/")[-1]
        if pos=="nr" and nextpos!="nr":
            new_line+=w+"/"+pos+" "
            SURNAME=False
            #print(w)
            continue
        if pos=="nr" and nextpos=="nr":
            #print(w)
            if SURNAME:
                SURNAME=False
            else:
                SURNAME=True
            if SURNAME:
                new_line+=w+"_"
            else:
                new_line+=w+"/"+pos+" "
    new_line=new_line.strip()
    #print(new_line)
    out.write("%s\n" % new_line)
        




def deal_file(filepath,outname):
    #f=codecs.open(filepath,"r",encoding="GB2312")
    f=codecs.open(filepath,"r",encoding="GB18030")
    out=codecs.open(outname,"w+",encoding="utf-8")
    line=f.readline()
    line=line.strip()
    idx=1
    while line:
        print(idx)
        line=line.strip()
        if line:
            deal_sentence(line,out)
        idx+=1
        line=f.readline()


    #for line in f:
    #    line=line.strip()
    #    if not line:
    #        continue
    #    deal_sentence(line,out)
    f.close()
    out.close()


if __name__=='__main__':
    rootdir="199801.txt"
    outname="199801_BIOS.txt"
    deal_file(rootdir,outname)





