/*************************************************************************
	> File Name: Scentence.h
	> Author: 
	> Mail: 
	> Created Time: 2017年06月07日 星期三 09时02分55秒
 ************************************************************************/

#ifndef _SCENTENCE_H
#define _SCENTENCE_H

#include<vector>
#include<iostream>
#include<string>
#include "Entity.h"

class Sentence{
public:

    Sentence()=default;
    Sentence(std::vector<std::string> tk, std::vector<std::string> lbl): tokens(tk), labels(lbl) { }
    std::string generateWhole();
    Sentence &addWholeToken(std::string token, std::string lbl);
    ~Sentence()=default;
    void clear()
    { whole_tokens.clear(); whole_labels.clear(); tokens.clear();labels.clear(); }

private:
    std::vector<Entity> ents{Entity(),Entity(),Entity()};
    std::vector<std::string> tokens;
    std::vector<std::string> labels;
    std::vector<std::string> whole_tokens{""};
    std::vector<std::string> whole_labels{""};

};

inline Sentence &Sentence::addWholeToken(std::string token, std::string lbl)
{
    whole_tokens.push_back(token);
    whole_labels.push_back(lbl);
}


inline std::string Sentence::generateWhole()
{
    std::string line="";
    std::string name="";
    std::string loc="";
    std::string organ="";
    whole_tokens.clear();
    whole_labels.clear();
    for(size_t i=0; i<labels.size(); i++)
    {
        if(labels[i]=="B-Nr"){
            ents[0].clear();
            ents[0].addIdx(i);
        }
        if(labels[i]=="I-Nr"){
            ents[0].addIdx(i);
        }
        if(labels[i]=="E-Nr"){
            ents[0].addIdx(i);
            size_t nn=ents[0].lblIdxs.size();
            if(ents[0].lblIdxs.back()-ents[0].lblIdxs[0]==nn-1) {
                for(size_t j=ents[0].lblIdxs[0]; j<=ents[0].lblIdxs.back(); j++)
                    name+=tokens[j];
                addWholeToken(name,"Nr");
                ents[0].clear();
                name="";
            }
        }
        if(labels[i]=="S-Nr"){
            addWholeToken(tokens[i],"Nr");
            ents[0].clear();
            name="";
        }


        if(labels[i]=="B-Ns"){
            ents[1].clear();
            ents[1].addIdx(i);
        }
        if(labels[i]=="I-Ns"){
            ents[1].addIdx(i);
        }
        if(labels[i]=="E-Ns"){
            ents[1].addIdx(i);
            size_t nn=ents[1].lblIdxs.size();
            if(ents[1].lblIdxs.back()-ents[1].lblIdxs[0]==nn-1) {
                for(size_t j=ents[1].lblIdxs[0]; j<=ents[1].lblIdxs.back(); j++)
                    loc+=tokens[j];
                addWholeToken(loc,"Ns");
                ents[1].clear();
                loc="";
            }
        }
        if(labels[i]=="S-Nr"){
            addWholeToken(tokens[i],"Ns");
            ents[1].clear();
            loc="";
        }


        if(labels[i]=="B-Nt"){
            ents[2].clear();
            ents[2].addIdx(i);
        }
        if(labels[i]=="I-Nt"){
            ents[2].addIdx(i);
        }
        if(labels[i]=="E-Nt"){
            ents[2].addIdx(i);
            size_t nn=ents[2].lblIdxs.size();
            if(ents[2].lblIdxs.back()-ents[2].lblIdxs[0]==nn-1) {
                for(size_t j=ents[2].lblIdxs[0]; j<=ents[2].lblIdxs.back(); j++)
                    organ+=tokens[j];
                addWholeToken(organ,"Nt");
                ents[2].clear();
                organ="";
            }
        }
        if(labels[i]=="S-Nt"){
            addWholeToken(tokens[i],"Nt");
            ents[2].clear();
            organ="";
        }

        if(labels[i]=="O"){
            if (ents[0].lblIdxs.size()>0)
                for(auto it=ents[0].lblIdxs.begin(); it!=ents[0].lblIdxs.end(); ++it)
                    addWholeToken(tokens[*it],labels[*it]);
            if (ents[1].lblIdxs.size()>0)
                for(auto it=ents[1].lblIdxs.begin(); it!=ents[1].lblIdxs.end(); ++it)
                    addWholeToken(tokens[*it],labels[*it]);
            if (ents[2].lblIdxs.size()>0)
                for(auto it=ents[2].lblIdxs.begin(); it!=ents[2].lblIdxs.end(); ++it)
                    addWholeToken(tokens[*it],labels[*it]);
            addWholeToken(tokens[i],labels[i]);
            ents[0].clear();
            ents[1].clear();
            ents[2].clear();
            name="";
            loc="";
            organ="";

        }



    }

    for(size_t i=0; i<whole_labels.size(); ++i)
        if(i==whole_labels.size()-1)
            line+=whole_tokens[i]+"/"+whole_labels[i];
        else
            line+=whole_tokens[i]+"/"+whole_labels[i]+" ";
    return line;
}


#endif
