#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
import tensorflow as tf
import argparse
import numpy as np
import codecs

LABELS=['O','B-Nr','I-Nr','E-Nr','S-Nr','B-Ns','I-Ns','E-Ns','S-Ns','B-Nt','I-Nt','E-Nt','S-Nt']
N_CLASSES=13

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
                if len(nr.lbl_idxs)>0:
                    for i in nr.lbl_idxs:
                        self.whole_tokens.append(self.tokens[i])
                        self.whole_labels.append(self.labels[i])
                if len(ns.lbl_idxs)>0:
                    for i in ns.lbl_idxs:
                        self.whole_tokens.append(self.tokens[i])
                        self.whole_labels.append(self.labels[i])
                if len(nt.lbl_idxs)>0:
                    for i in nt.lbl_idxs:
                        self.whole_tokens.append(self.tokens[i])
                        self.whole_labels.append(self.labels[i])
                self.whole_tokens.append(self.tokens[idx])
                self.whole_labels.append(lbl)
                nr.clear()
                ns.clear()
                nt.clear()
                name=""
                loc=""
                organ=""



def initialize_vocabulary(w2v_path):
    with codecs.open(w2v_path,"r",encoding="utf-8") as f:
        line=f.readline().strip()
        ss=line.split()
        total=int(ss[0])
        dim=int(ss[1])
        print("total:%d,dim:%d" %(total,dim) )
        vocab=[line.strip().split()[0] for line in f]
        vocab.append('unk')
        #print(vocab)
        #for i,item in enumerate(vocab):
        #    print(i,":",item)
        vocab_dict=dict( [(x,y+1) for (y,x) in enumerate(vocab)])
        #print(vocab_dict)
        return vocab_dict,vocab

def load_graph(frozen_graph_filename):
    # We parse the graph_def file
    with tf.gfile.GFile(frozen_graph_filename,"rb") as f:
        graph_def=tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # We load the graph_def in the default graph 
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, input_map=None, return_elements=None, name="prefix", op_dict=None, producer_op_list=None)
    return graph 

def ids_to_words(ids,vob):
    words=[ vob[idx-1] for idx in ids]
    return words

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
        
def wtoids(vocab_dict,words,sentence_len):
    x=[]
    ids=[vocab_dict[w] for w in words]
    nn=len(ids)
    for i in range(nn,sentence_len):
        ids.append(0)
    x.append(ids)
    return np.array(x)


def test_evaluate(sess,logits_op,x,tX,xlength,vob,sentence_len):
    logits_=sess.run(logits_op,feed_dict={x:tX })
    logits_=np.reshape(logits_,(-1,sentence_len,N_CLASSES))
    # logits_ shape [batch_size,n_step,n_classes] xlength[batch_size] tX[batch_size,n_step]
    for logit,length_,input_ in zip(logits_,xlength,tX):
        input_=input_[:length_]
        logit=logit[:length_]
        # logit shape [n_step,n_classes]
        labels=[np.where(taglist==np.max(taglist))[0][0] for taglist in logit]
        # labels shape [length_]
        line=ids_labels_to_words(input_,vob,labels)
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

        

def main(frozen_model_filename,filename,sentence_len,w2v_path,model_out_path):
    #加载已经将参数固化后的图
    graph=load_graph(frozen_model_filename)

    # We can list operations
    # op.values() gives you a list of tensors it produces
    # op.name gives you the name
    # 输入，输出结点也是opeartion，所以，我们可以得到operation的名字
    #for op in graph.get_operations():
        #print(op.name,op.values)

    # 操作有:prefix/Placeholder/inputs_placeholder
    # 操作有:prefix/Accuracy/predictions
    # 为了预测，我们需要找到我们需要feed的tensor，那么就需要该tensor的名字
    # 注意 prefix/Placeholder/inputs_placeholder 仅仅是操作的名字，prefix/Placeholder/inputs_placeholder:0才是tensor的名字
    x=graph.get_tensor_by_name('prefix/input_placeholder:0')
    logits=graph.get_tensor_by_name('prefix/infer_head:0')

    vob_dict,vob=initialize_vocabulary(w2v_path)
    model_out=codecs.open(model_out_path,"w+",encoding="utf-8")
    
    with tf.Session(graph=graph) as sess:
        count=0
        with codecs.open(filename,"r",encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                count+=1
                print(line)
                words=[w for w in line]
                #print(words)
                #for w in words:
                #    print("%s" % w)
                xlength=[]
                line_len=len(words)
                if line_len>80:
                    continue
                xlength.append(line_len)
                tX=wtoids(vob_dict,words,sentence_len)
                #test_evaluate(sess,logits,length,transMatrix,x,tX,xlength,vob,model_out)
                test_evaluate(sess,logits,x,tX,xlength,vob,sentence_len)
        model_out.close()



if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--word2vec_path",default="char_vec_50.txt",type=str, help="word2vec_path")
    parser.add_argument("--frozen_model_filename",default="logs/frozen_model.pb",type=str, help="Frozen model file to import")
    parser.add_argument("--test_data_path",default="test.txt",type=str, help="Frozen model file to import")
    parser.add_argument("--model_out_path",default="model_out.txt",type=str, help="model output path")
    parser.add_argument("--max_sentence_len",default=80,type=str, help="Frozen model file to import")
    args=parser.parse_args()
    sentence_len=int(args.max_sentence_len)
    print("sentence_len:",sentence_len)
    filename=args.test_data_path
    w2v_path=args.word2vec_path
    model_out_path=args.model_out_path
    main(args.frozen_model_filename,filename,sentence_len,w2v_path,model_out_path)
        
    print("finish")












