#!/usr/bin/env python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())
import codecs
import re

def split_sentence(filepath,outname):
    f=codecs.open(filepath,"r",encoding="utf-8")
    out=codecs.open(outname,"w+",encoding="utf-8")
    for line in f:
        line=line.strip()
        #print(line)
        if not line:
            continue
        #sentences=line.split("。")
        #print(len(sentences))
        #fields=re.split(r"(。)\s+/w",line)
        fields=re.split(r"(。|？|！|；)\s*/w",line.encode("utf-8"))
        #print(len(fields))
        if len(fields)<4:
            #print(line)
            out.write("%s\n" % line)
            continue
        values=fields[::2]
        delimiters=fields[1::2]
        for val,symbol in zip(values,delimiters):
            #print("%s%s" % (val.strip()+" ",symbol+"/w"))
            out.write("%s%s\n" % (val.strip()+" ",symbol+"/w"))
    f.close()
    out.close()



if __name__=='__main__':
    rootdir="199801_BIOS.txt"
    outname="199801_BIOS_sentence.txt"
    split_sentence(rootdir,outname)


