# file parameters
TRA_PREFIX = 'txStatis'
TRA_FROM = 1001
TRA_TO = 1002

class simulator:
    def __init__(self):
        self.data = []

    def get_tranfer(self):
        for i in range(TRA_FROM, TRA_TO):
            with open(TRA_PREFIX + str(i), 'r') as f:
                for l in f:
                    temp = l.split()
                    if len(temp) == 4:
                        if temp[3] == '0x':
                            self.data.append(l)

    def output(self, fp):
        with open(fp, 'w') as f:
            f.writelines(self.data)

if __name__ == "__main__":
    simu = simulator()
    out_fp = 'transfer1'
    simu.get_tranfer()
    simu.output(out_fp)
