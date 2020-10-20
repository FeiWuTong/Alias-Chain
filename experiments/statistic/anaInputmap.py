class analysis:
    def __init__(self):
        self.amap = {}
        self.newadd = 0

    def read_ori(self, fp):
        with open(fp, 'r') as f:
            for l in f:
                self.amap[l.split()[0]] = 0

    def analysis_newadd(self, fp):
        with open(fp, 'r') as f:
            for l in f:
                temp = l.split()
                k = temp[0]
                if k not in self.amap.keys():
                    self.newadd += (len(k) - 2) / 2
                    self.newadd += len(temp[-1]) / 2
                    temp = temp[1:-1]
                    for i in range(len(temp)):
                        if i % 2:
                            self.newadd += len(temp[i]) / 2
                        else:
                            self.newadd += int(temp[i]) / 2

    def output(self):
        print(self.newadd)

if __name__ == "__main__":
    fp_ori = 'amaptop1'
    fp_new = 'amaptop12'
    ana = analysis()
    ana.read_ori(fp_ori)
    ana.analysis_newadd(fp_new)
    ana.output()