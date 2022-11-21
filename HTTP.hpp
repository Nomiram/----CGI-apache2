#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <map>

class HTTP
{
    public:
    std::map<std::string,std::string> getparams;
    std::map<std::string,std::string> postparams;
    std::map<std::string,std::string> cookie;
    std::map<std::string,std::string> outcookie;
	private:
	std::stringstream OUT;

	public:
	HTTP();
	void init();
	void send();
    HTTP(std::string query, std::string postdata);
	std::string httpGet(std::string name);
	std::string httpPost(std::string name);
	std::string getCookie(std::string name);
	std::string setCookie(std::string name, std::string value);
	~HTTP();
   //private:
	
};