#include "Server.h"

	string socketIO::read(){
		char c=0;
		size_t i=0;
		string s="";
		while(c!='\n'){
			recv(clientID,&c,sizeof(char),0);
			s+=c;
		}
		return s;
	}
	void socketIO::write(string text){
		const char* txt=text.c_str();
		send(clientID,txt,strlen(txt),0);		
	}

	void socketIO::write(float f){
		ostringstream ss;
		ss <<f;
		string s(ss.str());		
		write(s);
	}

	void socketIO::read(float* f){
		//recv(clientID,f,sizeof(float),0);
		// it will be already in the string line
	}


Server::Server(int port) {
	  stopped=false;
	  fd=socket(AF_INET,SOCK_STREAM,0);
	  if(fd<0)
		throw "socket failed";

	  server.sin_family = AF_INET;
	  server.sin_addr.s_addr = INADDR_ANY;
	  server.sin_port = htons(port);

	  if(bind(fd,(struct sockaddr*)&server, sizeof(server))<0)
		throw "bind failure";

	  if(listen(fd, 3)<0)
		throw "listen failure";
}

void sigHandler(int sigNum){
	// for future implementations
}

void Server::start(ClientHandler& ch) {	
    int filesID = 0;
	signal(SIGALRM,sigHandler);
		    while(!stopped){
				socklen_t clientSize=sizeof(client);
				alarm(1);
				int aClient = accept(fd,(struct sockaddr*)&client,&clientSize);
				cout << "client is connected\n"
					 << endl;
				if(aClient>0){
					new thread([&aClient,this,&ch, &filesID](){
						ch.handle(aClient, filesID);
						close(aClient);
					});
                    ++filesID;
				}
				alarm(0);

		    }
		    close(fd);

	//   t = new thread([&ch,this](){
	// 	    signal(SIGALRM,sigHandler);
	// 	    while(!stopped){
	// 			socklen_t clientSize=sizeof(client);
	// 			alarm(1);
	// 			int aClient = accept(fd,(struct sockaddr*)&client,&clientSize);
	// 			if(aClient>0){
	// 				//new thread([&aClient,this,&ch](){
	// 					ch.handle(aClient);
	// 					close(aClient);
	// 				//});
	// 			}
	// 			alarm(0);

	// 	    }
	// 	    close(fd);
	//   });
}

void Server::stop(){
	stopped=true;
	t->join(); // do not delete this!
}

Server::~Server() {
	// TODO Auto-generated destructor stub
}