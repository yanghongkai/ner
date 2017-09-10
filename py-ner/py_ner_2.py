# coding:utf-8
# __author__ = 'yhk'

from __future__ import print_function

import os
import sys
import codecs
import numpy as np
print(sys.getdefaultencoding())
reload(sys)
sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())

LABELS=['O','B-Nr','I-Nr','E-Nr','S-Nr','B-Ns','I-Ns','E-Ns','S-Ns','B-Nt','I-Nt','E-Nt','S-Nt']

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

    def addToken(self,token,label):
        self.tokens.append(token)
        self.labels.append(label)

    def clear(self):
        self.tokens=[]
        self.labels=[]
        self.whole_tokens=[]
        self.whole_labels=[]

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

def batch_load_data(lines,sentence_len):
    x=[]
    y=[]
    xlength=[]
    #print("sentence_len*2:",sentence_len*2)
    for line in lines:
        line=line.strip()
        if not line:
            continue
        ss=line.split(" ")
        assert(len(ss)==(sentence_len*2))
        lx=[]
        ly=[]
        length=0
        for i in xrange(sentence_len):
            lx.append(int(ss[i]))
            ly.append(int(ss[i+sentence_len]))
            if int(ss[i])>0:
                length+=1
        x.append(lx)
        y.append(ly)
        xlength.append(length)
    # return np.array(x),np.array(y),np.array(xlength)
    return x[0],y[0],xlength[0]



innode=50
hidenode=100
nclasses=13

class switch(object):
    def __init__(self, value):
        self.value=value
        self.fail=False
    def __iter__(self):
        """Return the mathch method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fail or not args:
            return True
        elif self.value in args:
            self.fail=True
            return True
        else:
            return False

def sigmoid(x):
    s=1.0/(1.0+np.exp(-1.0*x))
    return s

def ids_labels_to_words(ids,vob,lbls):
    global LABELS
    labels=[]
    line=""
    words=[ vob[idx-1] for idx in ids]
    for idx in lbls:
        labels.append(LABELS[idx])
    for (word,label) in zip(words,labels):
        line+=word+"/"+label+" "
    line=line.strip()
    return line

# print(np.__version__)
class LSTM():
    def __init__(self):
        global innode,hidenode,nclasses
        self.w=np.zeros((innode+hidenode,hidenode*4))
        print(self.w.shape)
        self.rw=np.zeros((innode+hidenode,hidenode*4))
        self.b=np.zeros(hidenode*4)
        self.rb=np.zeros(hidenode*4)

        self.softmax_w=np.zeros((hidenode*2,nclasses))
        self.softmax_b=np.zeros(nclasses)
        self.transitions=np.zeros((nclasses,nclasses))
        #
        # print(self.softmax_w.shape)
        self.w2v_path="char_vec_50.txt"
        self.embedding_path="w2v.txt"
        self.load_parameters()
        self.wid_dict,self.vob=self.initialize_vocabulary()
        self.build_embedding()

        # test load parameters
        # wi
        # print("test softmax_w:")
        # print(self.softmax_w)
        # print(self.softmax_w.shape)
        # successful


    def load_parameters(self):
        str1 = "fw/w"
        str2 = "fw/biases"

        str3 = "bw/w"
        str4 = "bw/biases"

        str5 = "softmax/w"
        str6 = "softmax/bias"
        str7 = "transitions"
        op = 0
        nrow=0
        ncol=0
        # f=codecs.open("modelpara_1.txt","r",encoding="utf-8")
        f=codecs.open("modelpara.txt","r",encoding="utf-8")
        for line in f:
            line=line.strip()
            if line==str1:
                op=1
                nrow=0
                continue
            if line==str2:
                op=2
                nrow=0
                continue
            if line==str3:
                op=3
                nrow=0
                continue
            if line==str4:
                op=4
                nrow=0
                continue
            if line==str5:
                op=5
                nrow=0
                continue
            if line==str6:
                op=6
                nrow=0
                continue
            if line==str7:
                op=7
                nrow=0
                continue

            for case in switch(op):
                if case(1):
                    self.w[nrow]=np.asarray(line.split(),dtype=np.float)
                    break
                if case(2):
                    self.b=np.asarray(line.split(),dtype=np.float)
                    break
                if case(3):
                    self.rw[nrow]=np.asarray(line.split(),dtype=np.float)
                    break
                if case(4):
                    self.rb=np.asarray(line.split(),dtype=np.float)
                    break
                if case(5):
                    self.softmax_w[nrow]=np.asarray(line.split(),dtype=np.float)
                    break
                if case(6):
                    self.softmax_b=np.asarray(line.split(),dtype=np.float)
                    break
                if case(7):
                    self.transitions[nrow]=np.asarray(line.split(),dtype=np.float)
                    break
                if case(0):
                    break
            nrow+=1


        print(self.w.shape)
        print(self.b.shape)
        print(self.rw.shape)
        print(self.rb.shape)
        print(self.softmax_w.shape)
        print(self.softmax_b.shape)
        print(self.transitions.shape)

    def initialize_vocabulary(self):
        with codecs.open(self.w2v_path,"r",encoding="utf-8") as f:
            line=f.readline().strip()
            ss=line.split()
            total=int(ss[0])
            dim=int(ss[1])
            print("total:%d,dim:%d" %(total,dim) )
            vocab=[line.strip().split()[0] for line in f]
            vocab.append('unk')
            # print("vocab:")
            # print(vocab)
            # print(len(vocab))
            # print(vocab[0],vocab[1],vocab[2],vocab[-1])
            # print(vocab[8867-1])
            #for i,item in enumerate(vocab):
            #    print(i,":",item)
            vocab_dict=dict( [(x,y+1) for (y,x) in enumerate(vocab)])
            # print(vocab_dict)
            # print("vocab_dict")
            # print(vocab_dict['unk'])
            return vocab_dict,vocab

    def build_embedding(self):
        self.embedding=[]
        f=codecs.open(self.embedding_path,"r",encoding="utf-8")
        for line in f:
            line=line.strip()
            if not line:
                continue
            self.embedding.append([ float(val) for val in line.split()])
        print(len(self.embedding))


    def lstmcell(self,sentence_embedding):
        sen_len=len(sentence_embedding)
        h_arr=np.empty((sen_len,hidenode))
        # print(h_arr.shape)
        pre_c=np.zeros(hidenode,dtype=np.float)
        pre_h=np.zeros(hidenode,dtype=np.float)
        for idx,w_embedding in enumerate(sentence_embedding):
            xt=np.array(w_embedding)
            # print(xt.shape)
            # print("xt:")
            # print(xt)
            # print("pre_h")
            # print(pre_h)
            xc=np.append(xt,pre_h)
            # print(xc.shape)
            # print(xc)
            # print(self.wi)
            # print(self.wi.shape)
            gate_sum=np.dot(xc,self.w)+self.b
            # print("gate_sum:")
            # print(gate_sum.shape)
            # print(gate_sum)
            i,j,f,o=np.split(gate_sum,4)

            # print("i:")
            # print(i.shape)
            # print(i)
            # i=np.dot(xc,self.wi)+self.bi
            # j=np.dot(xc,self.wj)+self.bj
            # f=np.dot(xc,self.wf)+self.bf
            # o=np.dot(xc,self.wo)+self.bo
            c=pre_c*sigmoid(f+1.0)+sigmoid(i)*np.tanh(j)
            h=np.tanh(c)*sigmoid(o)
            # h=np.tanh(c)*sigmoid(o)
            # print("state:")
            # print(c)
            # print("hidden:")
            # print(h)
            h_arr[idx]=h
            prec=c
            pre_h=h

            # print(i.shape)
            # print(i)
            # print(sigmoid(i))
            # print(f)
            # print(f+1.0)
            # break
        # print(h_arr)
        return h_arr




    def inference(self):
        # str=u"菲律宾爆发马拉维危机民众举家逃离"
        # str=u"中共中央总书记习近平来北京语言大学视察工作"
        # str=u"当地时间2017年5月24日，菲律宾棉兰老岛伊利甘，菲律宾爆发马拉维危机，马拉维市多处设施遭恐怖分子占领，民众逃离家园，经过伊利甘市入口的检查站。"
        # str=u"中共中央总书记、国家主席、中央军委主席、中央全面深化改革领导小组组长习近平10月11日下午主持召开中央全面深化改革领导小组第二十八次会议并发表重要讲话。"
        # str=u"美国马里兰大学学生杨舒平5月21日在毕业典礼上应邀演讲，从政治学专业的角度，谈到中美空气质量的亲身体会，以及自由、真相等话题。"
        # str=u"刚从劈腿风波中渐渐走出的谢杏芳在“520网络情人节”时突然发文称“见到小三上去给两个耳光,我谢谢你。”疑似开撕第三者。"
        str=u"北京语言大学大数据与语言教育技术研究所研究生在241教室听荀恩东关于中文句法语义分析的报告"

        sentence_embedding=[]
        sentence_ids=[]

        for c in str:
            print(c)
            id=self.wid_dict[c]
            sentence_ids.append(id)
            w_embedding=self.embedding[id]
            sentence_embedding.append(w_embedding)
            # print(id)
            # print(w_embedding)
        print(len(sentence_embedding))
        h_arr=self.lstmcell(sentence_embedding)
        h_arr_back=self.lstmcell(sentence_embedding[::-1])
        h_arr_b=h_arr_back[::-1]
        # print("h_arr_b")
        # print(h_arr_b.shape)
        # print(h_arr_b)
        lstm_h=np.concatenate((h_arr,h_arr_b),axis=1)
        # print(lstm_h.shape)
        # print(lstm_h)
        logit=np.dot(lstm_h,self.softmax_w)+self.softmax_b
        # print("logit:")
        # print(logit.shape)
        # print(logit)

        trellis=np.zeros_like(logit)
        backpointers=np.zeros_like(logit,dtype=np.int32)
        trellis[0]=logit[0]
        socres=logit
        #print("trellis:")
        print(trellis.shape)
        #print(trellis)

        for t in range(1,trellis.shape[0]):
            v=np.expand_dims(trellis[t-1],1)+self.transitions
            # print("v:")
            # print(v.shape)
            # print(v)
            # print("max:")
            # print(np.max(v,0))
            trellis[t]=logit[t]+np.max(v,0)
            # print("argmax:")
            # print(np.argmax(v,0))
            backpointers[t]=np.argmax(v,0)
            # break

        viterbi=[np.argmax(trellis[-1])]
        #print("viterbi:")
        #print(viterbi)
        #print("backpointers:")
        #print(backpointers)
        #print("backpointers[1:]")
        #print(backpointers[1:])
        #print("reversed(backpointers[1:])")
        #print(reversed(backpointers[1:]))
        for bp in reversed(backpointers[1:]):
            # print(bp)
            viterbi.append(bp[viterbi[-1]])
        #print("viterbi:")
        #print(viterbi)
        viterbi.reverse()
        print("viterbi reverse:")
        print(viterbi)
        # viterbi=[int(i) for i in viterbi]
        # print(viterbi)
        line=ids_labels_to_words(sentence_ids,self.vob,viterbi)
        print(line)

        sentence=Sentence()
        line=line.strip()
        for token in line.split():
            sentence.addToken(token.split('/')[0],token.split('/')[-1])
        sentence.generate_whole()
        nerline=""
        for w,lbl in zip(sentence.whole_tokens,sentence.whole_labels):
            nerline+=w+'/'+lbl+" "
        nerline=nerline.strip()
        print("%s" % nerline)

        #print("trellis")
        #print(trellis)
        #print(trellis.shape)
        viterbi_score=np.max(trellis[-1])
        #print("viterbi_score:")
        #print(viterbi_score)

    def inference_1(self,sentence_ids,tY):

        sentence_embedding=[]
        for id in sentence_ids:
            w_embedding=self.embedding[id]
            sentence_embedding.append(w_embedding)

        print(len(sentence_embedding))
        h_arr=self.lstmcell(sentence_embedding)
        h_arr_back=self.lstmcell(sentence_embedding[::-1])
        h_arr_b=h_arr_back[::-1]
        # print("h_arr_b")
        # print(h_arr_b.shape)
        # print(h_arr_b)
        lstm_h=np.concatenate((h_arr,h_arr_b),axis=1)
        # print(lstm_h.shape)
        # print(lstm_h)
        logit=np.dot(lstm_h,self.softmax_w)+self.softmax_b
        # print("logit:")
        # print(logit.shape)
        # print(logit)

        trellis=np.zeros_like(logit)
        backpointers=np.zeros_like(logit,dtype=np.int32)
        trellis[0]=logit[0]
        socres=logit
        #print("trellis:")
        print(trellis.shape)
        #print(trellis)

        for t in range(1,trellis.shape[0]):
            v=np.expand_dims(trellis[t-1],1)+self.transitions
            # print("v:")
            # print(v.shape)
            # print(v)
            # print("max:")
            # print(np.max(v,0))
            trellis[t]=logit[t]+np.max(v,0)
            # print("argmax:")
            # print(np.argmax(v,0))
            backpointers[t]=np.argmax(v,0)
            # break

        viterbi=[np.argmax(trellis[-1])]
        #print("viterbi:")
        #print(viterbi)
        #print("backpointers:")
        #print(backpointers)
        #print("backpointers[1:]")
        #print(backpointers[1:])
        #print("reversed(backpointers[1:])")
        #print(reversed(backpointers[1:]))
        for bp in reversed(backpointers[1:]):
            # print(bp)
            viterbi.append(bp[viterbi[-1]])
        #print("viterbi:")
        #print(viterbi)
        viterbi.reverse()
        print("viterbi reverse:")
        print(viterbi)
        # viterbi=[int(i) for i in viterbi]
        # print(viterbi)
        line=ids_labels_to_words(sentence_ids,self.vob,viterbi)
        # print(line)

        sentence=Sentence()
        line=line.strip()
        for token in line.split():
            sentence.addToken(token.split('/')[0],token.split('/')[-1])
        sentence.generate_whole()
        nerline=""
        for w,lbl in zip(sentence.whole_tokens,sentence.whole_labels):
            nerline+=w+'/'+lbl+" "
        nerline=nerline.strip()
        # print("%s" % nerline)

        correct_line=ids_labels_to_words(sentence_ids,self.vob,tY)
        # print(correct_line)
        return line,correct_line

        #print("trellis")
        #print(trellis)
        #print(trellis.shape)
        viterbi_score=np.max(trellis[-1])
        #print("viterbi_score:")
        #print(viterbi_score)



if __name__=='__main__':
    lstm=LSTM()
    # lstm.inference()

    model_name="model_out.txt"
    correct_name="correct_out.txt"
    model_out=codecs.open(model_name,"w+",encoding="utf-8")
    correct_out=codecs.open(correct_name,"w+",encoding="utf-8")

    filename="test_1998_ids_80.txt"
    lines=[]
    count=0
    limit=1
    sentence_len=80
    with codecs.open(filename,"r",encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            lines.append(line)
            count+=1
            if count%limit==0:
                print("processing %d lines" % count)
                tX,tY,xlength=batch_load_data(lines,sentence_len)
                print(tX)

                # print(tX[:xlength])
                # print(tY[:xlength])
                # print(xlength)
                # test_evaluate(sess,logits,length,transMatrix,x,tX,tY,xlength,vob,model_out,correct_out)
                model_line,correct_line=lstm.inference_1(tX[:xlength],tY[:xlength])
                print(model_line)
                print(correct_line)
                model_out.write("%s\n" % (model_line))
                correct_out.write("%s\n" % (correct_line))
                lines=[]
            # break





















