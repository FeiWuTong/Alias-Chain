class common:
    def __init__(self):
        self.data = []
        self.read_pos = 0
        self.deal = []
        self.mask = []
        self.all_data = 0
        self.common_data = 0
        self.id = []
        self.gen_id_cond = 5

    def read_data(self, fp):
        with open(fp, 'r') as f:
            self.data = f.readlines()

    def analyse_data(self):
        lines = len(self.data)
        # only judge_prefix same can be recognized as the same group
        judge_prefix = 10
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
                        self.id.append((cur_len - 2) / 2)
                    cur_j += 1
                    same_cnt += 1
                elif self.data[cur_j][:judge_prefix] == cur_input[:judge_prefix]:
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
                self.id.append((self.common_length() - 2) / 2)
            '''
            if len(self.deal):
                self.deal.append(cur_input)
                self.make_mask()
                # 3 sample should not take into calculation (i.e. more than 3 times call can be take into consideration)
                self.common_data += (self.common_length() - 2) * (len(self.deal) - 1) / 2
                self.id.append((self.common_length() - 2) / 2)
            '''
            # next round
            cur_i = cur_j
            self.deal = []

    def output(self):
        print("All data bytes: %d" % self.all_data)
        print("Common data bytes: %d" % self.common_data)
        print("ID amount: %d" % len(self.id))
        print("Total ID bytes: %d" % sum(self.id))

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
        # just for test
        '''
        test = ""
        for i in range(m_length):
            if self.mask[i]:
                test += m_std[i]
        print(m_std)
        print(test)
        '''

    # find out common length in self.mask
    def common_length(self):
        return self.mask.count(1)

if __name__ == "__main__":
    fp = 'contract_top_5'
    com = common()
    com.read_data(fp)
    print(len(com.data))
    com.analyse_data()
    com.output()