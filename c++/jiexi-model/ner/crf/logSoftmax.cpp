/*************************************************************************
	> File Name: vec_m.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年06月08日 星期四 18时51分25秒
 ************************************************************************/

#include<iostream>
#include<vector>
#include<cmath>
using namespace std;

vector<double>& logSoftmax(vector<double>& vec)
{
    double total=0.0;
    for(size_t i=0;i<vec.size();i++)
        total+=exp(vec[i]);
    for(size_t i=0;i<vec.size();i++)
        vec[i]-=total;
    return vec;
    
}


int main()
{
    vector<vector<double>> vec{vector<double>(3,0.1),vector<double>(3,0.5)};
    for(size_t i=0;i<vec.size();i++)
    {
        for(size_t j=0;j<vec[i].size();j++)
            cout<<vec[i][j]<<" ";
        cout<<endl;
    }
    for(size_t i=0;i<vec.size();i++)
    {
        vec[i]=logSoftmax(vec[i]);
    }
    for(size_t i=0;i<vec.size();i++)
    {
        for(size_t j=0;j<vec[i].size();j++)
            cout<<vec[i][j]<<" ";
        cout<<endl;
    }

    return 0;
}





