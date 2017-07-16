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
    double d;
}SD;

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
    for(size_t i=0; i<states.size();i++)
    {

        SD objs=T[states[i]];
        cout<<"states: "<<states[i]<<" start p :"<<objs.d<<endl;
    }

    for(size_t i=1; i<obs.size();i++)
    {
        map<string,SD> U;
        for(size_t j=0;j<states.size(); j++)
        {
            string argmax="";
            double valmax=0.0;
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
            cout<<" path: "<<SD_tmp.s<<" p: "<<SD_tmp.d<<endl;
        }
        T=U;
    }
    string argmax="";
    double valmax=0.0;
    double prob=1.0;
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
    cout<<"return s: "<<SD_tmp.s<<" return p: "<<SD_tmp.d<<endl;
    return SD_tmp;
}

int main()
{
    vector<vector<double>> emit_p{ {0.5,0.4,0.1},{0.1,0.3,0.6}};
    cout<<"emit_p: "<<endl;
    for(size_t i=0; i<emit_p.size(); i++)
    {
        for(size_t j=0; j<emit_p[i].size();j++)
            cout<<emit_p[i][j]<<" ";
        cout<<endl;
    }

    vector<vector<double>> trans_p{{0.7,0.3},{0.4,0.6} };
    cout<<"trans_p: "<<endl;
    for(size_t i=0; i<trans_p.size(); i++)
    {
        for(size_t j=0; j<trans_p[i].size();j++)
            cout<<trans_p[i][j]<<" ";
        cout<<endl;
    }
    vector<double> start_p{0.6,0.4};
    cout<<"start_p: "<<endl;
    for(size_t i=0; i<start_p.size(); i++)
        cout<<start_p[i]<<" ";
    cout<<endl;

    vector<string> states{"Healthy","Fever"};
    cout<<"states: "<<endl;
    for(size_t i=0; i<states.size(); i++)
        cout<<states[i]<<" ";
    cout<<endl;

    vector<string> obs{"norm","cold","dizzy"};
    cout<<"obs: "<<endl;
    for(size_t i=0; i<obs.size(); i++)
        cout<<obs[i]<<" ";
    cout<<endl;

    SD ret=forward_viterbi(obs,states,start_p,trans_p,emit_p);
    cout<<ret.s<<endl;
    cout<<ret.d<<endl;

    
    return 0;
}






