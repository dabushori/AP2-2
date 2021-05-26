

#ifndef CLI_H_
#define CLI_H_

#include "commands.h"
#include <algorithm>
#include <string.h>
#include <vector>

using namespace std;

class CLI {
  vector<Command *> commands;
  DefaultIO *dio;

public:
  CLI(DefaultIO *dio);
  void start(int filesID);
  virtual ~CLI();
};

#endif /* CLI_H_ */
