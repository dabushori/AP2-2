/*
 * Server.h
 *
 *  Created on: Dec 13, 2020
 *      Author: Eli
 */

#ifndef SERVER_H_
#define SERVER_H_

#include <iostream>
#include <netinet/in.h> // The header file in.h contains constants and structures needed for internet domain addresses.
#include <sys/socket.h> // The header file socket.h includes a number of definitions of structures needed for sockets.

#include <pthread.h>
#include <thread>

#include <signal.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "CLI.h"

using namespace std;

// edit your ClientHandler interface here:
class ClientHandler {
public:
  virtual void handle(int clientID, int filesID) = 0;
};

// you can add helper classes

class socketIO : public DefaultIO {
  int clientID;

public:
  socketIO(int clientID) : clientID(clientID) {}

  virtual string read();
  virtual void write(string text);

  virtual void write(float f);

  virtual void read(float *f);
  virtual int getID() { return clientID; }
};

// edit your AnomalyDetectionHandler class here
class AnomalyDetectionHandler : public ClientHandler {
public:
  virtual void handle(int clientID, int filesID) {
    socketIO sio(clientID);
    CLI cli(&sio);
    cli.start(filesID);
  }
};

struct ServerException : public std::exception {
  std::string s;
  ServerException(std::string ss) : s(ss) {}
  ~ServerException() throw() {} // Updated
  const char *what() const throw() { return s.c_str(); }
};

// implement on Server.cpp
class Server {
  // you may add data members
  int fd;
  sockaddr_in server;
  sockaddr_in client;

  thread *t;

  volatile bool stopped;

public:
  Server(int port);
  virtual ~Server();

  void start(ClientHandler &ch);

  void stop();

  int getID() { return fd; }
};

#endif /* SERVER_H_ */
