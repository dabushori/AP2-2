import socket

class AnomalyDetectionClient:
    def __init__(self, ip: str, port: int):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            self.sock.settimeout(1)
            print('connected to server')
            
        except Exception:
            print('error')
            if (self.sock):
                self.sock.close()


    def send_message(self, message: str):
        self.sock.send(message.encode()) # encode message


    def upload_files(self, path_to_learn_file: str, path_to_anomaly_file: str, is_hybrid: bool):
        print('uploading files')
        self.send_message('1\n')

        # send learn file
        f = open(path_to_learn_file, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            self.send_message(line)
        self.send_message('done\n')
        print('done uploading learn file')

        # send anomalies file
        f = open(path_to_anomaly_file, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            self.send_message(line)
        self.send_message('done\n')
        print('done uploading anomalies file')

        # activate the algorithm
        if (is_hybrid):
            self.send_message('3\n')
        else:
            self.send_message('4\n')
        
        # get the results
        self.send_message('5\n')
        
        # recieve until 'Done.'
        results = self.recieve_results()
        # while ...:
        #     results ...

        return self.parse_results(results)


    def recieve_results(self):
        res = ''
        msg = None
        try:
            while msg != '':
                msg = self.sock.recv(4096).decode()
                res += msg
        except socket.error:
            print('end of data')
        print('results: {}'.format(res))
        return res



    def parse_results(self, results: str):
        print(results)
        return 'end of parse_results' # parsed_results


    def close(self):
        self.send_message('7\n')
        self.sock.close()


if __name__ == '__main__':
    c = AnomalyDetectionClient('192.168.1.125', 8080)
    res = c.upload_files('test/learn.csv', 'test/anomaly.csv', True)
    print(res)