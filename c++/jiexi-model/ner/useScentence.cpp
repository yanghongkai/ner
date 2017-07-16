/*************************************************************************
	> File Name: useScentence.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年06月07日 星期三 10时24分31秒
 ************************************************************************/
#include "Sentence.h"

#include<iostream>
#include<vector>
#include<string>
using namespace std;

int main()
{
    vector<string> tokens{"菲","律","宾","爆","发","马","拉","维","危","机","民","众","举","家","逃","离"};
    vector<string> labels{"B-Ns","I-Ns","E-Ns","O","O","B-Ns","I-Ns","E-Ns","O","O","O","O","O","O","O","O"};
    Sentence sentence(tokens,labels);
    string line=sentence.generateWhole();
    sentence.clear();
    cout<<line<<endl;
    return 0;
}













