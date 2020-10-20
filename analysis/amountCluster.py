class Cluster:
    def __init__(self):
        self.cluster = []
        self.cur = 0
        self.least = 5
    
    def read_data(self, fp):
        with open(fp, 'r') as f:
            self.data = list(map(int, f.readlines()))

    def clustering_lv1(self):
        length = len(self.data)
        i = 0
        while i < length:
            self.cur = self.data[i]
            if i + self.least < length and self.data[i + self.least] == self.cur:
                self.cluster.append([self.data[i], 1])
                j = i + self.least + 1
                while j < length and self.data[j] == self.cur:
                    j += 1
                self.cluster[-1][1] = j - i
                i = j
            else:
                i += 1

    def output_lv1(self):
        acc = 0
        for item in self.cluster:
            acc += item[1]
        print("[LV1 cluster] total clusters: %d" % len(self.cluster))
        print("[LV1 cluster] clusters' elements: %d" % acc)

    def output_lv1_file(self, fp):
        with open(fp, 'w') as f:
            f.writelines(list(map(lambda x: x + '\n', self.cluster)))

    def pre_conflation(self):
        if len(self.data) == 0:
            return
        self.xy = [[self.data[0], 0]]
        for item in self.data:
            if item == self.xy[-1][0]:
                self.xy[-1][1] += 1
            else:
                self.xy.append([item, 1])

    def output_xy(self, fp):
        with open(fp, 'w') as f:
            f.writelines([str(item[0]) + ' ' + str(item[1]) + '\n' for item in self.xy])

    def judge_in_cluster(self, amount):
        pass

if __name__ == "__main__":
    fp = 'AmountSort'
    out_file = 'Amount_cluster'
    is_lv1 = False
    clus = Cluster()
    clus.read_data(fp)
    if is_lv1:
        clus.clustering_lv1()
        clus.output_lv1()
        clus.output_lv1_file(out_file)
    else:
        xy_file = 'Amount_xy'
        clus.pre_conflation()
        clus.output_xy(xy_file)
