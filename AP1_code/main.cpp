#include "Server.h"
#include <iostream>
#include <filesystem>

using namespace std;

int main(int argc, char* argv[]) {
	if (argc != 2) {
		cout << "Usage: ./a.out <port num>"
			 << endl;
		return 0;
	}
	int port;
	try
	{
		port = stoi(argv[1]);
	} catch(invalid_argument) {
		cout << "the port entered is not a number" << endl;
		return 0;
	}
	try {
		auto filesDir = filesystem::current_path();
		filesDir /= "files";
		if (!filesystem::is_directory(filesDir)) {
			filesystem::create_directory(filesDir);
		}

		AnomalyDetectionHandler h;
		Server server(port);
		server.start(h);
	} catch(const char* c) {
		cout << c << endl;
	} catch (...) {
		cout << "An error occured" << endl;
	}
	return 0;
}