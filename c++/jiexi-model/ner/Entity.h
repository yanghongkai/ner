/*************************************************************************
	> File Name: Entity.h
	> Author: 
	> Mail: 
	> Created Time: 2017年06月07日 星期三 08时56分24秒
 ************************************************************************/

#ifndef _ENTITY_H
#define _ENTITY_H

#include<string>
#include<iostream>

class Entity{
public:
    Entity()=default;
    Entity &addIdx(size_t idx);
    ~Entity()=default;
    friend class Sentence;
    Entity &clear();
private:
    std::vector<size_t> lblIdxs;

};

inline Entity &Entity::addIdx(size_t idx)
{
    lblIdxs.push_back(idx);
    return *this;
}

inline Entity &Entity::clear()
{
    if(lblIdxs.size()>0)
        lblIdxs.clear();
    return *this;
}


#endif
