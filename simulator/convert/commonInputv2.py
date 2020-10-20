class common:
    def __init__(self):
        self.data = []
        self.deal = []
        self.mask = []
        self.all_data = 0
        self.common_data = 0
        self.id = {}
        self.gen_id_cond = 5
        # only judge_prefix same can be recognized as the same group
        self.judge_prefix = 10
        self.increse = 0

    def id_ret(self, inc):
        return "{:04x}".format(inc)

    def read_data(self, fp):
        with open(fp, 'r') as f:
            self.data = f.read().splitlines()

    def analyse_data(self):
        lines = len(self.data)
        cur_i = 0
        while cur_i < lines:
            cur_input = self.data[cur_i]
            cur_len = len(cur_input)
            cur_j = cur_i + 1
            same_cnt = 0
            while cur_j < lines:
                if len(self.data[cur_j]) != cur_len:
                    break
                if self.data[cur_j] == cur_input:
                    if same_cnt == self.gen_id_cond:
                    #if same_cnt == 0:
                        self.id[cur_input] = [self.id_ret(self.increse)]
                        self.increse += 1
                    cur_j += 1
                    same_cnt += 1
                elif self.data[cur_j][:self.judge_prefix] == cur_input[:self.judge_prefix]:
                    # 1 : pre-calculate same part
                    self.common_data += same_cnt * (cur_len - 2) / 2
                    same_cnt = 0
                    # 2 : append to deal list and update cur_input
                    self.deal.append(cur_input)
                    cur_input = self.data[cur_j]
                    cur_j += 1
                else:
                    break
            # calculate all data and common data
            self.all_data += (cur_j - cur_i) * (cur_len - 2) / 2
            if same_cnt:
                self.common_data += same_cnt * (cur_len - 2) / 2
            
            if len(self.deal) >= self.gen_id_cond:
                self.deal.append(cur_input)
                self.make_mask()
                # 3 sample should not take into calculation (i.e. more than 3 times call can be take into consideration)
                self.common_data += (self.common_length() - 2) * (len(self.deal) - self.gen_id_cond) / 2
                self.mask2map()
            # next round
            cur_i = cur_j
            self.deal = []

    def output_map(self, fp):
        with open(fp, 'w') as f:
            for k in self.id.keys():
                item = " ".join(self.id[k])
                f.write(k + " " + item + "\n")

    def output(self):
        print("All data bytes: %d" % self.all_data)
        print("Common data bytes: %d" % self.common_data)
        print("ID keys: %d" % len(self.id.keys()))

    # make mask for self.deal
    def make_mask(self):
        if len(self.deal) <= 1:
            return
        m_std = self.deal[0]
        m_len = len(m_std)
        self.mask = [1] * m_len
        for item in self.deal:
            for i in range(m_len):
                if self.mask[i]:
                    if item[i] != m_std[i]:
                        self.mask[i] = 0

    def mask2map(self):
        map_value = []
        map_key = self.deal[0][:self.judge_prefix]
        cur_len = len(self.deal[0])
        last_zero = self.judge_prefix
        last_one = self.judge_prefix
        cur_pos = self.judge_prefix
        zero = True

        while cur_pos < cur_len:
            if self.mask[cur_pos] == 1:
                if zero:
                    map_value.append(str(cur_pos - last_zero))
                    zero = False
                last_zero = cur_pos + 1
            else:
                if zero == False:
                    map_value.append(self.deal[0][last_one:cur_pos])
                    zero = True
                last_one = cur_pos + 1
            cur_pos += 1
        map_value.append(self.id_ret(self.increse))
        self.increse += 1

        self.id[map_key] = map_value

    # find out common length in self.mask
    def common_length(self):
        return self.mask.count(1)

if __name__ == "__main__":
    fp = 'contract_top_1'
    out = 'amaptop1'
    com = common()
    com.read_data(fp)
    com.analyse_data()
    com.output()
    com.output_map(out)