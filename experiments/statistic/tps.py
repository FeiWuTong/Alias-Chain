class tps:
    def __init__(self):
        self.data = []
        self.total = 0
        self.txs = 0
        self.cumu = 0
        self.block = 0

    def read_data(self, fp):
        with open(fp, 'r') as f:
            self.data = f.readlines()

    def process(self, totalsize):
        self.total = totalsize
        for item in self.data:
            temp = item.split()
            if int(temp[1]) == 0:
                continue
            self.cumu += int(temp[0])
            self.txs += int(temp[1])
            self.block += 1
            if self.cumu > self.total:
                self.cumu -= int(temp[0])
                self.txs -= int(temp[1])
                self.block -= 1
                break
        print("Total %d blocks" % self.block)
        print("Total %d txs" % self.txs)
        print("Total %d block size" % self.cumu)

    def processN(self, bn):
        for item in self.data:
            temp = item.split()
            if int(temp[1]) == 0:
                continue
            self.cumu += int(temp[0])
            self.txs += int(temp[1])
            self.block += 1
            if self.block == bn:
                break
        print("Total %d blocks" % self.block)
        print("Total %d txs" % self.txs)
        print("Total %d block size" % self.cumu)

    def cal_tps(self, blocksize, interval):
        blocknum = self.cumu / blocksize
        print(blocknum)
        blocktime = interval * blocknum
        return self.txs / blocktime

    def output(self, fp, name, blocksize, interval):
        with open(fp, 'a') as f:
            f.write("\n" + name + "\n")
            f.write("Set Total limit: %d\n" % self.total)
            f.write("Real cumulative size: %d\n" % self.cumu)
            f.write("Total txs count: %d\n" % self.txs)
            f.write("Blocksize: %d\n" % blocksize)
            f.write("Block create interval: %d\n" % interval)
            f.write("TPS: %.2f\n" % self.cal_tps(blocksize, interval))
            

if __name__ == "__main__":
    # parameters
    fp = 'blockStatis_sc'
    output_f = 'eth'
    name = 'eth'
    calN = False
    t = tps()
    t.read_data(fp)
    # calculation
    if calN:
        limit = 30000000
        bs = 300000
        interval = 15
        #t.process(limit)
        blocknum = 100
        t.processN(blocknum)
        t.output(output_f, name, bs, interval)
    else:
        blocknum = 75
        t.processN(blocknum)