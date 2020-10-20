class Sort:
    def __init__(self, threshold):
        self.threshold = threshold
        self.data = []

    def read_data(self, fp):
        with open(fp, 'r') as f:
            tempdata = f.readlines()
        for item in tempdata:
            (addr, cnt) = item.split()
            if int(cnt) >= self.threshold:
                self.data.append(addr + '\n')

    def output_file(self, fp):
        with open(fp, 'w') as f:
            f.writelines(self.data)

if __name__ == "__main__":
    threshold = 87
    in_file = 'DBToOutput_4'
    out_file = 'to_87_4'
    mysort = Sort(threshold)
    mysort.read_data(in_file)
    mysort.output_file(out_file)