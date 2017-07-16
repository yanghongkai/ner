/*************************************************************************
	> File Name: ner_predict.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年05月29日 星期一 09时25分43秒
 ************************************************************************/

#include<iostream>
#include<map>
#include<vector>
#include<fstream>
#include<sstream>
using namespace std;

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
    ifstream vocab_file("char_vec_50_1.txt");
    auto vocab_map=buildMap(vocab_file);
    for (const auto &w:vocab_map)
        cout<<w.first<<" : "<<w.second<<endl;
    vocab_file.close();
    vocab_file.open("char_vec_50_1.txt");
    auto vocab_vec=buildVector(vocab_file);
    for(auto it=vocab_vec.begin(); it!=vocab_vec.end(); it++)
        cout<<*it<<" ";
    vocab_file.close();
    cout<<endl;
    return 0;
}



















