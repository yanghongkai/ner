/*************************************************************************
	> File Name: w2ids.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年06月06日 星期二 10时43分31秒
 ************************************************************************/

#include<iostream>
#include<string>
#include<fstream>
#include<vector>
#include<map>
using namespace std;


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

int main()
{
    
    ifstream vocab_file("char_vec_50.txt");
    //ifstream vocab_file("char_vec_50_1.txt");
    auto vocab_map=buildMap(vocab_file);
    //for (const auto &w:vocab_map)
      //  cout<<w.first<<" : "<<w.second<<endl;
    vocab_file.close();
   

    vocab_file.open("char_vec_50.txt");
    //vocab_file.open("char_vec_50_1.txt");
    auto vocab_vec=buildVector(vocab_file);
    //for(auto it=vocab_vec.begin(); it!=vocab_vec.end(); it++)
      //  cout<<*it<<" ";
    vocab_file.close();
    cout<<endl;

    ifstream in("test.txt");
    string line;
    size_t max_sentence_len=80;
    vector<int> w2ids(max_sentence_len,0);

    if(!in.is_open())
    {
        cout<<"Error opening file";
        exit(1);
    }

    while(!in.eof())
    {
        if(getline(in,line))
        {
            cout<<line<<endl;
            auto wstr=chStr(line);
            size_t length=0;
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
        }
    }
    return 0;
}






