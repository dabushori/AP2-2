import socket
import json
import os
import shutil

class AnomalyDetectionClient:
    def __init__(self, ip: str, port: int):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            
        except Exception:
            print('error')
            if (self.sock):
                self.sock.close()


    def send_message(self, message: str):
        self.sock.send(message.encode()) # encode message


    def detect_anomalies(self, path_to_learn_file: str, path_to_anomaly_file: str, is_hybrid: bool):
        self.send_message('1\n')

        # send learn file
        f = open(path_to_learn_file, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            self.send_message(line)
        self.send_message('done\n')

        # send anomalies file
        f = open(path_to_anomaly_file, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            self.send_message(line)
        self.send_message('done\n')

        # activate the algorithm
        if (is_hybrid):
            self.send_message('3\n')
        else:
            self.send_message('4\n')
        
        # get the results
        self.send_message('5\n')
        results = self.recieve_results()

        return self.parse_results(results)


    def recieve_results(self):
        res_lines = []
        res = ''
        msg = None
        while 'Done.' not in res_lines:
            msg = self.sock.recv(4096).decode()
            res += msg
            res_lines = res.split('\n')
            # res_lines.extend(msg.split('\n'))
        start = res_lines.index('Results:') + 1
        end = res_lines.index('Done.')
        return res_lines[start:end]


    def parse_results(self, results: list):
        # to implement
        anomalies = []
        for line in results:
            d = {}
            splits = line.split('\t')
            i = 1
            for word in splits :
                if i == 1 :
                    d["time_step"] = word
                if i == 2 :
                    d["property_1"] = word
                if i == 3 :
                    d["property_2"] = word
                i += 1
            anomalies.append(d)
        dictonary = {"anomalies" : anomalies}
        return dictonary # parsed_results


    def close(self):
        self.send_message('7\n')
        self.sock.close()

resultsCounter = 0

class AnomalyDetector:
    def __init__(self, server_ip: str, server_port: int):
        self.results_counter = 0
        self.server_ip = server_ip
        self.server_port = server_port

        self.results_dir = os.path.join('model', 'results')
        if os.path.isdir(self.results_dir):
            shutil.rmtree(self.results_dir)
        os.mkdir(self.results_dir)
        

    def detect_anomalies(self, pathToLearnFile: str, pathToAnomaliesFile: str, is_hybrid: bool):
        client = AnomalyDetectionClient(self.server_ip, self.server_port)
        res = client.detect_anomalies(pathToLearnFile, pathToAnomaliesFile, is_hybrid)
        client.close()
        name = os.path.join(self.results_dir, 'results{}.json'.format(self.results_counter))
        with open(name, 'w') as fp:
            json.dump(res, fp)
        self.results_counter += 1
        return name