class aver:
    def __init__(self):
        self.idmap = {}
        self.checkmap = {}
        self.addr = 20
        self.cnt = 0
        self.total = 0
        self.ave = 0
        self.txs = 11000
        self.id2txs = 0

    def read_check(self, fp):
        with open(fp, 'r') as f:
            for l in f:
                to = l.split()[1]
                if to not in self.checkmap.keys():
                    self.checkmap[to] = 1
                else:
                    self.checkmap[to] += 1
    
    def read_id(self, fp):
        with open(fp, 'r') as f:
            for l in f:
                temp = l.split()
                self.idmap[temp[0]] = (len(temp[1]) - 2) / 2

    def compare(self):
        for k in self.checkmap.keys():
            if k in self.idmap.keys():
                if self.checkmap[k] >= 2 or self.idmap[k] <= 2:
                    self.total += self.addr + self.idmap[k]
                    self.cnt += 1
                    self.id2txs += self.checkmap[k]
        self.ave = self.total * 1.0 / self.txs

    def output(self):
        print("Total: %d" % self.total)
        print("IDCount: %d" % self.cnt)
        print("Txs: %d" % self.txs)
        print("Average: %d" % self.ave)
        print("id2txs: %d" % self.id2txs)

if __name__ == "__main__":
    fp_check = 'sm_transfer1'
    fp_id = 'AddrIdMap10'
    ave = aver()
    ave.read_check(fp_check)
    ave.read_id(fp_id)
    ave.compare()
    ave.output()