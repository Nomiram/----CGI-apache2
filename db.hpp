#ifndef __DB__HPP__CLASS__
#define __DB__HPP__CLASS__
#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <map>
/*
добавление записи, удаление, просмотр списка, просмотр одной записи.
Записи в базе данных хранятся построчно в файле, а отдельные поля записи разделены символами-разделителями.
*/
template<typename KeyType, typename ValType>
class FILEDB{
    public:
    FILEDB();
    FILEDB(std::string filename);
    ~FILEDB();
    int write(KeyType key, ValType value);
    ValType read_one(KeyType key);
    std::map<KeyType,ValType>* read_all();
    int erase(KeyType key);
    private:
    std::string dbfilename;
};

#endif