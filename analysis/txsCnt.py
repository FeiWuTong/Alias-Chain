class Sort:
    def __init__(self):
        self.cnt = 0

    def read_data(self, fp):
        with open(fp, 'r') as f:
            tempdata = f.readlines()
        for item in tempdata:
            self.cnt += int(item.split()[1])

    def read_data2(self, fp, top):
        if top == 0:
            return
        with open(fp, 'r') as f:
            for line in f:
                top -= 1
                self.cnt += int(line)
                if top == 0:
                    return

    def output_cnt(self):
        print(self.cnt)

if __name__ == "__main__":
    in_file = 'DBToOutput_2'
    in_file2 = 'SortedFTAddr_2'
    top = 991
    mysort = Sort()
    mysort.read_data2(in_file2, top)
    mysort.output_cnt()