/*************************************************************************
	> File Name: ner_predict.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年05月29日 星期一 09时25分43秒
 ************************************************************************/
#include "tensorflow/core/public/session.h"
#include "tensorflow/core/platform/env.h"
#include "Sentence.h"

#include<iostream>
#include<map>
#include<vector>
#include<fstream>
#include<sstream>
#include<string>
#include<algorithm>
#include<cmath>

using namespace std;
using namespace tensorflow;

typedef struct SD
{
    string s;
    double d;
}SD;

vector<string> split(string str,string pattern)
{
    string::size_type pos;
    vector<string> result;
    str+=pattern; //扩展字符串以方便操作

    int size=str.size();

    for(int i=0;i<size;i++)
    {
        pos=str.find(pattern,i);
        if(pos<size)
        {
            string s=str.substr(i,pos-i);
            result.push_back(s);
            i=pos+pattern.size()-1;
        }
    }
    return result;
}
vector<string> chStr(string str)  //输入str字符串，依次输出分隔好的chr，chr为linux默认的utf8
{
    //string str;  //一串包含汉字的字串
    string strChar;  //str中的一个汉字
    vector<string> wstr;
    for(int i=0; str[i]!='\0'; )
    {
        char chr=str[i];
        //chr 是 0xxx xxxx，即ascii编码
        if((chr & 0x80)==0)
        {
            strChar=str.substr(i,1);
            wstr.push_back(strChar);
            ++i;
        }//chr是1111 1xxx
        else if((chr & 0xF8)==0xF8)
        {
            strChar=str.substr(i,5);
            wstr.push_back(strChar);
            i+=5;
        }//chr是1111 xxxx
        else if((chr & 0xF0)==0xF0)
        {
            strChar=str.substr(i,4);
            wstr.push_back(strChar);
            i+=4;
        }//chr是111x xxxx
        else if((chr & 0xE0)==0xE0)
        {
            strChar=str.substr(i,3);
            wstr.push_back(strChar);
            i+=3;
        }//chr是11xx xxxx
        else if((chr & 0xC0)==0xC0)
        {
            strChar=str.substr(i,2);
            wstr.push_back(strChar);
            i+=2;
        }
    }
    return wstr;
}

map<string, size_t> buildMap(ifstream &map_file)
{
    map<string,size_t> vocab_map;
    string key;
    string value;
    getline(map_file,value);
    size_t idx=1;
    while(map_file>>key && getline(map_file,value)){
        vocab_map[key]=idx;
        idx++;
    }
    vocab_map["unk"]=idx;
    return vocab_map;
}

vector<string> buildVector(ifstream &map_file)
{
    vector<string> vocab_vec;
    string key;
    string value;
    getline(map_file,value);
    while(map_file>>key && getline(map_file,value)){
        vocab_vec.push_back(key);
    }
    vocab_vec.push_back("unk");
    return vocab_vec;
}

string idsLabelsToWords(vector<string> wStr, vector<int> lblIdx, vector<string> LABEL)
{
    string line;
    for(size_t i=0;i<lblIdx.size(); i++)
        line+=wStr[i]+"/"+LABEL[lblIdx[i]]+" ";
    return line;
}


SD  forward_viterbi(vector<string> obs, vector<string> states, vector<double> start_p, vector<vector<double>> trans_p, vector<vector<double>> emit_p)
{
    map<string,SD> T;
    SD SD_tmp;
    for(size_t i=0;i<states.size();i++)
    {
        SD_tmp.s=states[i];
        SD_tmp.d=start_p[i]*emit_p[i][0];
        T[states[i]]=SD_tmp;
    }
   
    /*
    for(size_t i=0; i<states.size();i++)
    {

        SD objs=T[states[i]];
        cout<<"states: "<<states[i]<<" start p :"<<objs.d<<endl;
    }
    */
    

    for(size_t i=1; i<obs.size();i++)
    {
        map<string,SD> U;
        for(size_t j=0;j<states.size(); j++)
        {
            string argmax="";
            double valmax=-1e300;
            string v_path="";
            
            for(size_t k=0; k<states.size();k++)
            {
                double p=T[states[k]].d*trans_p[k][j]*emit_p[j][i];
                v_path=T[states[k]].s;
                if(p>valmax)
                {
                    argmax=v_path+","+states[j];
                    valmax=p;
                }
            }
            SD_tmp.s=argmax;
            SD_tmp.d=valmax;
            U[states[j]]=SD_tmp;
            //cout<<" path: "<<SD_tmp.s<<" p: "<<SD_tmp.d<<endl;
        }
        T=U;
        //cout<<"i= "<<i<<"***************************************"<<endl;
    }
    string argmax="";
    double valmax=-1e300;
    string v_path="";
    double v_prob=1.0;
    for(size_t i=0;i<states.size();i++)
    {
        SD objs=T[states[i]];
        v_path=objs.s;
        v_prob=objs.d;
        if(v_prob>valmax)
        {
            argmax=v_path;
            valmax=v_prob;
        }
    }
    SD_tmp.s=argmax;
    SD_tmp.d=valmax;
    //cout<<"return s: "<<SD_tmp.s<<" return p: "<<SD_tmp.d<<endl;
    return SD_tmp;
}

vector<double>& logSoftmax(vector<double>& vec)
{
    double total=0.0;
    for(size_t i=0;i<vec.size();i++)
        total+=exp(vec[i]);
    total=log(total);
    for(size_t i=0;i<vec.size();i++)
        vec[i]=vec[i]-total;
    return vec;
    
}
vector<double>& expSoftmax(vector<double>& vec)
{
    double total=0.0;
    for(size_t i=0;i<vec.size();i++)
        total+=exp(vec[i]);
    for(size_t i=0;i<vec.size();i++)
        vec[i]=exp(vec[i])/total;
    return vec;
}
    
int main()
{
    vector<string> LABEL={"O","B-Nr","I-Nr","E-Nr","S-Nr","B-Ns","I-Ns","E-Ns","S-Ns","B-Nt","I-Nt","E-Nt","S-Nt"};


    ifstream vocab_file("char_vec_50.txt");
    auto vocab_map=buildMap(vocab_file);
    //for (const auto &w:vocab_map)
      //  cout<<w.first<<" : "<<w.second<<endl;
    vocab_file.close();
    vocab_file.open("char_vec_50.txt");
    auto vocab_vec=buildVector(vocab_file);
    //for(auto it=vocab_vec.begin(); it!=vocab_vec.end(); it++)
      //  cout<<*it<<" ";
    vocab_file.close();

    // Initialize a tensorflow session
    cout<<"start initalize session"<<"\n";
    Session* session;
    Status status=NewSession(SessionOptions(),&session);
    if(!status.ok()){
        cout<<status.ToString()<<endl;
        return 1;
    }

    //Read in the protobuf graph we exported
    GraphDef graph_def;
    status=ReadBinaryProto(Env::Default(),"./frozen_model.pb",&graph_def);
    if(!status.ok()){
        cout<<status.ToString()<<endl;
        return 1;
    }

    //Add the graph to the session
    status=session->Create(graph_def);
    if(!status.ok()){
        cout<<status.ToString()<<endl;
        return 1;
    }

    cout<<"preparing input data..."<<endl;
    size_t sentences_size=1;
    size_t max_sentence_len=80;
    size_t num_classes=13;
    vector<int> w2ids(max_sentence_len,0);

    ifstream test_file("test.txt");
    string line;
    if(!test_file.is_open())
    {
        cout<<"Error opeing test.txt";
        exit(1);
    }
    while(!test_file.eof())
    {
        if(getline(test_file,line))
        {
            cout<<line<<"\n";
            auto wstr=chStr(line);
            size_t length=0;
            vector<int> lblIdx;
            for(auto it=wstr.begin(); it!=wstr.end(); ++it,++length)
            {
                //cout<<*it<<"/";
                //cout<<vocab_map[*it]<<" ";
                w2ids[length]=vocab_map[*it];
            }
            //cout<<endl;
            cout<<"length: "<<length<<endl;
            //for(auto it=w2ids.begin(); it!=w2ids.end(); ++it)
              //  cout<<*it<<" ";
            //cout<<endl;
            //Setup inputs and outputs:
            Tensor x(DT_INT32,TensorShape({sentences_size,max_sentence_len}));
            //Tensor x(DT_INT32,TensorShape({1,80}));
            copy_n(w2ids.begin(),w2ids.size(),x.flat<int>().data());
            cout<<"data is ready"<<endl;
            vector<pair<string,Tensor>> inputs={
                {"input_placeholder",x} 
            };

            // The session will initalize the outputs
            vector<Tensor> outputs;
            //Run the session, evaluating our "infer_head" operation from the graph
            status=session->Run(inputs,{"softmax_1/unary_scores","transitions"}, {}, &outputs);
            if(!status.ok()){
                cout<<status.ToString()<<"\n";
                return 1;
            }else{
                cout<<"Success run !!!"<<"\n";
            }
            cout<<"output size:"<<outputs.size()<<endl;
            
            vector<vector<double>> emit_p(num_classes,vector<double>(length,0.0));
            vector<vector<double>> emit_tmp(length,vector<double>(num_classes,0.0));
            vector<vector<double>> trans_p(num_classes,vector<double>(num_classes,0.0));
            double init_p=1/double(num_classes);
            vector<double> start_p(num_classes,init_p);
            /** cout start_p */
            /*
            cout<<"start_p: "<<endl;
            for(int i=0;i<start_p.size();i++)
                cout<<start_p[i]<<" ";
            cout<<endl;
            */

            for(size_t idx=0; idx<outputs.size(); idx++)
            {
                if(idx%2==1)  //transitions
                {
                    cout<<"transitions:"<<endl;
                    auto items=outputs[idx].shaped<float,2>({num_classes,num_classes});
                    for(size_t i=0; i<num_classes; i++)
                    {
                        for(size_t j=0; j<num_classes; j++)
                        {
                            //cout<<items(i,j)<<" ";
                            trans_p[i][j]=items(i,j);
                        }
                        //cout<<endl;
                    }
                    for(size_t i=0;i<trans_p.size();i++)
                    {
                            trans_p[i]=expSoftmax(trans_p[i]);
                           // trans_p[i]=logSoftmax(trans_p[i]);
                    }
                    /** cout trans_p  */
                    /*
                    cout<<"trans_p: "<<endl;
                    for(size_t i=0;i<trans_p.size();i++)
                    {
                        for(size_t j=0;j<trans_p[i].size();j++)
                            cout<<trans_p[i][j]<<" ";
                        cout<<endl;
                    }
                    cout<<endl;
                    */
                    
                }
                else{  //logits
                    auto items=outputs[idx].shaped<float,2>({max_sentence_len,num_classes});
                    for(size_t i=0; i<length; i++)
                    {
                        for(size_t j=0; j<num_classes; j++)
                        {
                            //cout<<items(i,j)<<" ";
                            emit_tmp[i][j]=items(i,j);

                        }
                        //cout<<endl;
                    }
                    /** emit_p data transfer  */
                    for(size_t i=0;i<emit_tmp.size();i++)
                    {
                        emit_tmp[i]=expSoftmax(emit_tmp[i]);
                        //emit_tmp[i]=logSoftmax(emit_tmp[i]);
                    }
                     /** end emit_p transfer  */
                     for(size_t i=0;i<emit_tmp.size();i++)
                        for(size_t j=0;j<emit_tmp[i].size();j++)
                            emit_p[j][i]=emit_tmp[i][j];
                    
                    /** cout emit_p */
                    /*
                    cout<<"emit_p: "<<endl;
                    for(size_t i=0;i<emit_p.size();i++)
                    {
                        for(size_t j=0;j<emit_p[i].size();j++)
                            cout<<emit_p[i][j]<<" ";
                        cout<<endl;
                    }
                    cout<<endl;
                    */
                    
                    /** end of cout emit_p */
                }
            }
            SD ret=forward_viterbi(wstr,LABEL,start_p,trans_p,emit_p);
            cout<<ret.s<<endl;
            //cout<<ret.d<<endl;
            auto labels=split(ret.s,",");
            Sentence sentence(wstr,labels);
            string nerLine=sentence.generateWhole();
            cout<<nerLine<<endl;
            sentence.clear();


        }
    }




    cout<<endl;
    return 0;
}



