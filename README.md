# AP2-2 - Ori Dabush and Yorai Roth Hazan
# Project Documentation

Our project is built from two parts.
## Part 1 - Anomaly Detection Web Application
A web application where the client can detect anomalies. The application sits in the address "localhost:8080/".

The client chooses a .csv file to learn from, a .csv file to detect anomalies in and an anomaly detection algorithm (hybrid or liner regression). After he uploads the files, the server will detect the anomalies and return the results. 

There are two options to view the results of the anomaly detection, based on which button the client chose:
* If the client chooses the "View Results As A JSON File" button, the results will be displayed as a raw JSON file.
* If the client chooses the "View Results In A Table" button, the results will be displayed as a nice table that contains 3 columns - the time step the anomaly occured at, the feature that the anomaly was detected at, and the most correlated feature to that feature.

To detect the anomalies, we use the action that will be described at the second part.

### How it works?
When the client enters the address "localhost:8080/" using his explorer, the server returns the index.html page (using generate_index_page method in the page generator module) and it will be shown to the client. 

Then, The user will be able to choose the files and the algorithm (using a html form) and upload the files to the server. The upload will be done to the "localhost:8080/detect" address so the anomaly detection action that will be described in the second part will handle it. The name of the submit button will tell the part 2 logic how to return the results - as a JSON file or as a table.

After the anomaly detection is ended, the results will be returned and will be displayed to the client in an inner frame inside the index.html page.

## Part 2 - Anomaly Detection Server
A server that responds to HTTP POST requests. The server listens at address "localhost:8080/detect".

The POST request must contain the following parameters:
* A .csv file to learn from.
* A .csv file to detect anomalies in.
* An anomaly detection algorithm - "hybrid" or "line_regression".

After the server recieves the request it detects the anomalies using the server we built in the previous semester. The server returns the results as a JSON file. 

The server also has an option to return the results as a html table, this option is used in the first part. The server does this by calling the genetrate_results_page in the page generator module with the JSON file name as a parameter.

### How it works?
The server saves both of the .csv files in the uploads folder and checks if the algorithm is hybrid or not. 

After that he calls the model method "detect_anomalies", which is implemented in the AnomalyDetector class in the anomaly_detection module inside the model part. 

This function recieves the files and the algorithm, uses the server from the first semester (by using the AnomalyDetectionClient class which will be explained later). The function saves the results in the results folder and return the name of the results file (a JSON file).

## AnomalyDetectionClient class
In the model part, we used the anomaly detection server from previous semester in order to detect the anomalies. The class that connects to the server and communicate with it is the AnomalyDetectionClient class. It recieves the IP and the port of the server from the previous semester. 

The detect_anomalies method in this class recieves the files and the algorithm, uses the server from the previous semester to detect the anomalies, saves the results as a JSON file in the results folder and returns the name of the JSON results file.

## File Hierarchy
```
│   AP2-2.csv
│   README.md
│   
├───AP1_code
│       AnomalyDetector.h
│       anomaly_detection_util.cpp
│       anomaly_detection_util.h  
│       CLI.cpp
│       CLI.h
│       commands.h
│       HybridAnomalyDetector.cpp
│       HybridAnomalyDetector.h
│       main.cpp
│       Makefile
│       minCircle.cpp
│       minCircle.h
│       MinCircleAnomalyDetector.cpp
│       MinCircleAnomalyDetector.h
│       Server.cpp
│       Server.h
│       SimpleAnomalyDetector.cpp
│       SimpleAnomalyDetector.h
│       test.py
│       timeseries.cpp
│       timeseries.h
│
├───controller
│   │   web_application.py
│   │
│   └───uploads
│
├───model
│   │   anomaly_detection.py
│   │
│   │
│   └───results
│
└───view
    │   page_generator.py
    │
    └───templates
            index.html
            results.html
```

* `AP2-2.csv` - The file with our details
* `README.md` - The documentation file you are currently reading
* `AP1_code` - The code of the previous application server.
* `controller` - The folder that contains the controller module.
  * `web_application.py` - The file that contains the definition of the application itself (all the route methods).
  * `uploads` - The folder that contains the files that the users uploading.
* `model` - The folder that contains the model module.
  * `anomaly_detection.py` - The file that contains the AnomalyDetectionClient and AnomalyDetection client and responsible for the anomaly detecting.
  * `results` - The folder that contains the results of the clients' requests.
* `view` - The folder that contains the view module.
  * `templates` - The folder that contains the templates of the website - the .html files.
  * `page_generator.py` - The file that contains the definitions of the genetrate_index_page and genetrate_results_page methods.

## Requirements and Operation Explaination
### Requirements for operating our server:
* An anomaly detection that runs on a linux machine (will be explained soon).
* Python 3.9.0 or higher - can be installed [here](https://www.python.org/downloads/).
* Flask 1.1.2 or higher - can be installed [here](https://flask.palletsprojects.com/en/1.1.x/installation/) or by using pip package installer.

### How to run our application?
1. Run the anomaly detection server from the previous semester. In order to do it, you will need to compile the code in the AP1_code and run it. Follow the following steps:
   1. In a linux machine, compile the files using the command:
   > g++ *.cpp -lpthread

   or use the Makefile we made for you and type the command:
   > make

   2. After that, run the a.out file and give it the port you want the server to run on. For exmaple, if you want the server to run on port 8081 you need to run it like this:
   > ./a.out 8081

   **WARNING:** Pay attention that our server runs on port 8080 so make sure you don't use this port.

2. Run our application (from the AP2-2 directory), giving it the anomaly detection server and port as arguments. Do it using the command:
> path_to_python server_ip server_port

For example, if the anomaly detection server is running on the the current pc (localhost) on port 8081, run the command:
> python 127.0.0.1 8081

3. Enjoy our application by using your favorite browser (go to the address "localhost:8080/") or by sending it POST request as descried before.

### How to run our application on a new computer?
1. First, you need to get our code. You can get it [here](https://github.com/dabushori/AP2-2.git).

2. Then, you need to install python 3.9. Follow the installation guide in [this link](https://www.python.org/downloads/).

3. After you installed python 3.9, you need to install the flask module. Follow the installation guide in [this link](https://flask.palletsprojects.com/en/1.1.x/installation/).

4. Then, run our application by following the steps in the previous chapter.

## Links 
Take a look at the UML diagram that shows the structure of our project [here](https://github.com/dabushori/AP2-2/blob/main/UML.pdf).

Also, take a look at the explaination video we made [right over here]().