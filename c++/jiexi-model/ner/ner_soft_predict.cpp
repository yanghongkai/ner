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

using namespace std;
using namespace tensorflow;


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

    ifstream test_file("test1.txt");
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
                cout<<*it<<"/";
                cout<<vocab_map[*it]<<" ";
                w2ids[length]=vocab_map[*it];
            }
            cout<<endl;
            cout<<"length: "<<length<<endl;
            for(auto it=w2ids.begin(); it!=w2ids.end(); ++it)
                cout<<*it<<" ";
            cout<<endl;
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
            status=session->Run(inputs,{"infer_head"}, {}, &outputs);
            if(!status.ok()){
                cout<<status.ToString()<<"\n";
                return 1;
            }else{
                cout<<"Success run !!!"<<"\n";
            }

            for(vector<Tensor>::iterator it=outputs.begin(); it!=outputs.end(); ++it)
            {
                auto items=it->shaped<float,2>({max_sentence_len,num_classes});
                for(size_t i=0; i<length; i++)
                {
                    float max_val=items(i,0);
                    size_t max_idx=0;
                    for(size_t j=0; j<num_classes; j++)
                        if(items(i,j)>max_val)
                        {
                            max_val=items(i,j);
                            max_idx=j;
                        }
                    cout<<max_val<<" "<<max_idx<<endl;
                    lblIdx.push_back(max_idx);
                }
                cout<<endl;
                for(auto it=lblIdx.begin(); it!=lblIdx.end(); ++it)
                    cout<<*it<<" ";
                cout<<endl;
                vector<string> labels;
                for(auto it=lblIdx.begin(); it!=lblIdx.end(); ++it)
                    labels.push_back(LABEL[*it]);
                Sentence sentence(wstr,labels);
                string nerLine=sentence.generateWhole();
                cout<<nerLine<<endl;
                sentence.clear();

                //auto trans_line=idsLabelsToWords(wstr,lblIdx,LABEL);
                //cout<<trans_line<<endl;
            }

        }
    }




    cout<<endl;
    return 0;
}



















