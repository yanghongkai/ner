/*************************************************************************
	> File Name: crf_viterbi_decode.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年06月08日 星期四 12时32分49秒
 ************************************************************************/

#include<iostream>
#include<vector>
#include<string>
#include<map>
using namespace std;

typedef struct SD
{
    string s;
    float d;
}SD;

SD  forward_viterbi(vector<string> obs, vector<string> states, vector<float> start_p, vector<vector<float>> trans_p, vector<vector<float>> emit_p)
{
    map<string,SD> T;
    SD SD_tmp;
    for(size_t i=0;i<states.size();i++)
    {
        SD_tmp.s="";
        SD_tmp.d=start_p[i];
        T[states[i]]=SD_tmp;
    }
    for(size_t i=0; i<states.size();i++)
    {

        SD objs=T[states[i]];
        cout<<"states: "<<states[i]<<" start p :"<<objs.d<<endl;
    }

    for(size_t i=0; i<obs.size();i++)
    {
        map<string,SD> U;
        for(size_t j=0;j<states.size(); j++)
        {
            string argmax="";
            float valmax=0.0;
            float prob=1.0;
            string v_path="";
            float v_prob=1.0;
            for(size_t k=0; k<states.size();k++)
            {
                SD objs=T[states[k]];
                v_path=objs.s;
                v_prob=objs.d;
                float p=emit_p[k][i]*trans_p[k][j];
                prob*=p;
                v_prob*=p;
                if(v_prob>valmax)
                {
                    argmax=v_path+","+states[j];
                    valmax=v_prob;
                }
            }
            SD_tmp.s=argmax;
            SD_tmp.d=valmax;
            U[states[j]]=SD_tmp;
            cout<<" path: "<<SD_tmp.s<<" p: "<<SD_tmp.d<<endl;
        }
        T=U;
    }
    string argmax="";
    float valmax=0.0;
    float prob=1.0;
    string v_path="";
    float v_prob=1.0;
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
    cout<<"return s: "<<SD_tmp.s<<" return p: "<<SD_tmp.d<<endl;
    return SD_tmp;


int main()
{
    vector<vector<float>> emit_p{ {0.1,0.4,0.5},{0.6,0.3,0.1}};
    cout<<"emit_p: "<<endl;
    for(size_t i=0; i<emit_p.size(); i++)
    {
        for(size_t j=0; j<emit_p[i].size();j++)
            cout<<emit_p[i][j]<<" ";
        cout<<endl;
    }

    vector<vector<float>> trans_p{{0.7,0.3},{0.4,0.6} };
    cout<<"trans_p: "<<endl;
    for(size_t i=0; i<trans_p.size(); i++)
    {
        for(size_t j=0; j<trans_p[i].size();j++)
            cout<<trans_p[i][j]<<" ";
        cout<<endl;
    }
    vector<float> start_p{0.6,0.4};
    cout<<"start_p: "<<endl;
    for(size_t i=0; i<start_p.size(); i++)
        cout<<start_p[i]<<" ";
    cout<<endl;

    vector<string> states{"Rainy","Sunny"};
    cout<<"states: "<<endl;
    for(size_t i=0; i<states.size(); i++)
        cout<<states[i]<<" ";
    cout<<endl;

    vector<string> obs{"walk","shop","clean"};
    cout<<"obs: "<<endl;
    for(size_t i=0; i<obs.size(); i++)
        cout<<obs[i]<<" ";
    cout<<endl;

    SD ret=forward_viterbi(obs,states,start_p,trans_p,emit_p);
    cout<<ret.s<<endl;
    cout<<ret.d<<endl;

    
    return 0;
}






