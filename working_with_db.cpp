#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <sstream>
#include "HTTP.hpp"
#include "db.hpp"
#include "db.cpp"
using namespace std;
int main()
{
    HTTP http;
    http.init();
    FILEDB<std::string, std::string> db;
    std::string getparam = string(http.httpGet("get"));
    std::string getallparam = string(http.httpGet("getall"));
    if(http.httpGet("gui")!="false"){
        http.httpSendFile("db.html");
    }
    if (getparam != ""){
        http.setCookie("get", getparam);
        std::string res = db.read_one(getparam);
        if (res != ""){
            cout <<"{ \"" << getparam << "\": \"" <<http.escaping(res) << "\"}";
        }
    }
    if (getallparam != ""){
        std::map<string, string> *res = db.read_all();
        cout << "{";
        int i = 0;
        for (auto [key, val] : *res){
            if (i > 0){
                cout << ", ";
            }
            cout << "\"" << http.escaping(key) << "\": \"" << http.escaping(val) << "\"";
            i++;
        }
        cout << "}";
    }
    std::string setparam = string(http.httpPost("set"));
    if (setparam != ""){
        http.setCookie("get", setparam);
        int res = db.write(setparam, string(http.httpPost("value")));
        if (res == 0){
            cout << "{\"status\": [201, \"OK\"]}";
        }else{
            cout << "{\"status\": [500, \"Server Error\"]}";
        }
    }
    std::string eraseparam = string(http.httpPost("erase"));
    if (eraseparam != ""){
        int res = db.erase(eraseparam);
        if (res == 0){
            cout << "{\"status\": [201, \"OK\"]}";
        }else{
            cout << "{\"status\": [500, \"Server Error\"]}";
        }
    }
    http.send();
}
