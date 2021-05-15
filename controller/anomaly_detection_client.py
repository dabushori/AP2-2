import socket

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


    def upload_files(self, path_to_learn_file: str, path_to_anomaly_file: str, is_hybrid: bool):
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
        
        # recieve until 'Done.'
        results = self.recieve_results()
        # while ...:
        #     results ...

        return self.parse_results(results)


    def recieve_results(self):
        res_lines = []
        res = ''
        msg = None
        while 'Done.' not in res_lines:
            msg = self.sock.recv(4096).decode()
            res += msg
            res_lines.extend(msg.split('\n'))
        start = res_lines.index('Results:') + 1
        end = res_lines.index('Done.')
        return res_lines[start:end]



    def parse_results(self, results: list):
        print(results)
        return 'end of parse_results' # parsed_results


    def close(self):
        self.send_message('7\n')
        self.sock.close()


if __name__ == '__main__':
    c = AnomalyDetectionClient('', 8080)
    res = c.upload_files('test/learn.csv', 'test/anomaly.csv', True)
    print(res)