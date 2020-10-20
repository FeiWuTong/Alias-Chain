class conv:
    def __init__(self):
        self.amap = {}
        self.txs = []
        self.opcode = 10
    
    def read_map(self, fp):
        with open(fp, 'r') as f:
            for l in f:
                temp = l.split()
                self.amap[temp[0]] = temp[1:]

    def read_txs(self, fp):
        with open(fp, 'r') as f:
            for l in f:
                self.txs.append(l.split())

    def process_txs(self):
        for i in range(len(self.txs)):
            self.txs[i][3] = self.convert(self.txs[i][3])
    
    def convert(self, ori):
        if ori in self.amap.keys():
            return "0x" + self.amap[ori][-1]
        opcode = ori[:self.opcode]
        if opcode in self.amap.keys():
            value = self.amap[opcode]
            ret = ""
            start = self.opcode
            i = 0
            while i < len(value) - 1:
                ret += ori[start : (start + int(value[i]))]
                start += int(value[i])
                i += 1
                if i == len(value) - 1:
                    break
                cur_value_len = len(value[i])
                if ori[start : (start + cur_value_len)] != value[i]:
                    return ori
                start += cur_value_len
                i += 1
            if start != len(ori):
                ret += ori[start:]
            ret = "0x" + value[-1] + ret
            if len(ret) % 2 != 0:
                ret += "0"
            return ret
        return ori

    def output_txs(self, fp):
        with open(fp, 'w') as f:
            for item in self.txs:
                f.write(" ".join(item) + "\n")

if __name__ == "__main__":
    fp_map = 'amaptop1'
    fp_txs = 'contract1_smtx_native1'
    fp_out = 'contract1_smtx_conv11'
    c = conv()

    c.read_map(fp_map)
    c.read_txs(fp_txs)
    c.process_txs()
    c.output_txs(fp_out)