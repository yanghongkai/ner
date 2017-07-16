/*************************************************************************
	> File Name: split.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年06月08日 星期四 20时27分10秒
 ************************************************************************/

#include<iostream>
#include<string>
#include<vector>
using namespace std;

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


int main()
{
    string str("B-Ns,I-Ns,E-Ns,O,O");
    cout<<str.find(",",0)<<endl;
    vector<string> strspl=split(str,",");
    for(auto it=strspl.begin(); it!=strspl.end(); it++)
        cout<<*it<<"\t";
    cout<<endl;
    return 0;
}









