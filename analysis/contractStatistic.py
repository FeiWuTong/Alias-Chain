TRA_FROM = 501
TRA_TO = 1001
TRA_PREFIX = 'txStatis'

class statis:
    def __init__(self):
        self.data = {}

    def trace(self):
        for i in range(TRA_FROM, TRA_TO):
            with open(TRA_PREFIX + str(i), 'r') as f:
                temp = f.readlines()
            for line in temp:
                item = line.split()
                if len(item) == 4:
                    if item[1] != 'null' and item[3] != '0x':
                        self.data[item[1]] = 0

    def output(self):
        print(len(self.data))

if __name__ == "__main__":
    s = statis()
    s.trace()
    s.output()