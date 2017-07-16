/*************************************************************************
	> File Name: chStr.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年06月06日 星期二 12时25分40秒
 ************************************************************************/

#include<iostream>
#include<string>
#include<vector>
#include<fstream>
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

int main()
{
    ifstream in("test.txt");
    string line;
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
            for(auto it=wstr.begin(); it!=wstr.end(); ++it)
                cout<<*it<<" ";
            cout<<endl;
        }
    }
    return 0;
}





