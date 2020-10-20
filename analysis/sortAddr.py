import matplotlib.pyplot as plt
import numpy as np

class Sort:
    def __init__(self, fp = None):
        self.filepath = fp
        self.readlimit = 1000000
        self.data = []

    def set_filepath(self, fp):
        self.filepath = fp

    def read_data(self):
        pass

    def sort_data(self):
        pass

    def data_length(self):
        self.datalength = len(self.data)

    def transform_data(self):
        self.data = np.array(self.data)

    def output_file(self, fp):
        pass

# addr count statistic
class Addr(Sort):
    def read_data(self):
        with open(self.filepath, 'r') as f:
            for line in f:
                self.data.append(int(line.split()[1]))

    def output_file(self, fp):
        # default-fmt = '%.18e' makes output file large
        np.savetxt(fp, self.data, fmt = '%d')

    def sort_data(self):
        self.data.sort(reverse=True)

# addr sort and distribute id
# Input data: (unordered) addr \s count
# Output data: (desc order) addr \s id
# Request: sorted by count, and id ascending with 2 3 4 6 bytes
# Method1: only read count, after sorting can set count threshold for bytes (--used--)
# Method2: read whole addr(should use bytes array) and count into memory, than sorted in numpy.array
class Id(Sort):
    def __init__(self, fp = None):
        super(Id, self).__init__(fp)
        self.th = [0, 0, 0]
    
    def _set_id_start(self):
        self.id1 = 0
        self.id2 = 1 << ((self. id_len[1] << 3) - 2)    # 01
        self.id3 = 1 << ((self. id_len[2] << 3) - 1)    # 10
        self.id4 = (1 << ((self. id_len[3] << 3) - 2)) + (1 << ((self. id_len[3] << 3) - 1))    # 11
        self.id1_n = 0
        self.id2_n = 0
        self.id3_n = 0
        self.id4_n = 0

    def define_id(self, l):
        self.id_len = l
        self.id_cnt = list(map(lambda x: (1 << (x << 3) - 2), l))
        self._set_id_start()

    def read_threshold(self, fp):
        with open(fp, 'r') as f:
            '''
            for _ in range(self.id_cnt[0] - 1):
                f.readline()
            self.th1 = int(f.readline())
            for _ in range(self.id_cnt[0] - 1):
                f.readline()
            self.th2 = int(f.readline())
            '''
            tempdata = f.readlines()
            self.th[0] = int(tempdata[self.id_cnt[0]]) + 1
            self.th[1] = int(tempdata[self.id_cnt[1]]) + 1
            if (self.id_cnt[2] >= len(tempdata)):
                self.th[2] = 0
            else:
                self.th[2] = int(tempdata[self.id_cnt[2]]) + 1

    def set_threshold(self, th_l):
        self.th = th_l

    def output_threshhold(self):
        print("%d bytes id threshold: %d" % (self.id_len[0], self.th[0]))
        print("%d bytes id threshold: %d" % (self.id_len[1], self.th[1]))
        print("%d bytes id threshold: %d" % (self.id_len[2], self.th[2]))

    def read_data(self):
        with open(self.filepath, 'r') as f:
            for line in f:
                templine = line.split()
                self.data.append((templine[0], self._gen_id(int(templine[1]))))

    def _gen_id(self, cnt):
        tempid = 0
        if (cnt >= self.th[0] and self.id1_n < self.id_cnt[0]):
            str_f = '{}{}{}'.format("0x{:0>", self.id_len[0] << 1, "x}")
            tempid = str_f.format(self.id1)
            self.id1 += 1
            self.id1_n += 1
        elif (cnt >= self.th[1] and self.id2_n < self.id_cnt[1]):
            tempid = hex(self.id2)
            self.id2 += 1
            self.id2_n += 1
        else:
            tempid = hex(self.id3)
            self.id3 += 1
            self.id3_n += 1
        return tempid

    def output_file(self, fp):
        self.transform_data()
        np.savetxt(fp, self.data, fmt = '%s %s')

'''
class Amount(Sort):
    def read_data(self):
        pass

    def output_file(self, fp):
        pass
'''

class Draw:
    def __init__(self, fp = None):
        self.filepath = fp

    def set_filepath(self, fp):
        self.filepath = fp

    def read_data(self):
        self.data = np.loadtxt(self.filepath)

    def draw_pie(self):
        data = [0.0001, 0.001, 0.01, 0.1, 0.8889]
        labels = []
        explode=[0.0, 0.1, 0.2, 0.3, 0.4]
        length = len(self.data)
        for i in range(len(data)-1):
            labels.append(str(self.data[int(data[i]*length)*(-1)]))
        labels.append(labels[-1])
        for i in range(len(labels)-1):
            labels[i] = "> " + labels[i]
        labels[-1] = "< " + labels[-1]
        plt.pie(data, explode = explode, labels = labels, autopct='%1.2f%%')

        ''' reference
        plot2=plt.pie(data,                          # 每个饼块的实际数据，如果大于1，会进行归一化，计算percentage
                      explode=[0.0,0.1,0.2],               # 每个饼块离中心的距离
                      colors=['y','r','g'],               # 每个饼块的颜色
                      labels=['women','men','unknown'],   # 每个饼块的标签
                      labeldistance=1.2,                   # 每个饼块标签到中心的距离
                      autopct='%1.1f%%',                  # 百分比的显示格式
                      pctdistance=0.4,                     # 百分比到中心的距离
                      shadow=True,                         # 每个饼块是否显示阴影
                      startangle=0,                        # 默认从x轴正半轴逆时针起
                      radius=1.0                           # 饼块的半径
                      )
        '''
        plt.show()


if __name__ == '__main__':
    prefix = 'all_to'
    idoutput = 'AddrIdMap'
    suffix = 10
    output = 'SortedToAddr10_' + str(suffix)
    run_sort = False
    run_draw = False
    run_id = True
    id_len = (1, 2, 3, 4)
    # test or multi run
    #th_l = [207, 2]
    if run_sort:
        addr = Addr()
        addr.set_filepath(prefix + '_' + str(suffix))
        addr.read_data()
        addr.sort_data()
        addr.output_file(output)
        print("[sort] ok!")
    if run_draw:
        draw = Draw(output)
        draw.read_data()
        draw.draw_pie()
    if run_id:
        id_obj = Id()
        id_obj.define_id(id_len)
        id_obj.read_threshold(output)
        #id_obj.set_threshold(th_l)
        id_obj.output_threshhold()
        
        '''
        for i in range(suffix):
            id_obj.set_filepath(prefix + '_' + str(i+1))
            id_obj.read_data()
            id_obj.output_file(idoutput + str(i+1))
        '''
        id_obj.set_filepath(prefix + '_' + str(suffix))
        id_obj.read_data()
        id_obj.output_file(idoutput + str(suffix))
        
        print("[construct id] ok!")
