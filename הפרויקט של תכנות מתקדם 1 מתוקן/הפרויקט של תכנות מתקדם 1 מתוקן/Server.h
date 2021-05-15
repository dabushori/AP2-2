/*
 * Server.h
 *
 *  Created on: Dec 13, 2020
 *      Author: Eli
 */

#ifndef SERVER_H_
#define SERVER_H_

#include <iostream>
#include <sys/socket.h>  // The header file socket.h includes a number of definitions of structures needed for sockets.
#include <netinet/in.h>  // The header file in.h contains constants and structures needed for internet domain addresses.

#include <pthread.h>
#include <thread>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include<signal.h>
#include <sstream>

#include "CLI.h"

using namespace std;

// edit your ClientHandler interface here:
class ClientHandler{
    public:
    virtual void handle(int clientID)=0;
};

// you can add helper classes

class socketIO : public DefaultIO{
	int clientID;
public:

	socketIO(int clientID):clientID(clientID){}

	virtual string read();
	virtual void write(string text);

	virtual void write(float f);

	virtual void read(float* f);
};


// edit your AnomalyDetectionHandler class here
class AnomalyDetectionHandler:public ClientHandler{
	public:
    virtual void handle(int clientID){
    	socketIO sio(clientID);
    	CLI cli(&sio);
    	cli.start();
    }
};


// implement on Server.cpp
class Server {
	// you may add data members
	int fd;
	sockaddr_in server;
	sockaddr_in client;

	thread* t;

	volatile bool stopped;

public:
	Server(int port) throw (const char*);
	virtual ~Server();

	void start(ClientHandler& ch) throw (const char*);

	void stop();

	int getID() {
		return fd;
	}
};

#endif /* SERVER_H_ */
