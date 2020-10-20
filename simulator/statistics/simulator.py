# option parameters
TX_ADDR = 20
TX_SIGN = 65
TX_NONCE = 2
TX_GAS_A_PRICE = 7

# file parameters
DB1_PREFIX = 'DBToOutput'
DB2_PREFIX = 'DBFTOutput'
DB_CUR = 1
TRA_PREFIX = 'txStatis'
TRA_FROM = 901
TRA_TO = 1001
OUTPUT_FILE = 'simuResult'

# id threshold parameters (acquire from sortAddr.py)
ID_TO_TH1 = 75992
ID_TO_TH2 = 98
ID_TO_TH3 = 2
ID_FT_TH1 = 114841
ID_FT_TH2 = 247
ID_FT_TH3 = 4
ID1 = TX_ADDR - 1
ID2 = TX_ADDR - 2
ID3 = TX_ADDR - 3
ID4 = TX_ADDR - 4

# string decimal num transform to hex string's length
def s2HexL(s):
    try:
        temp_len = len(hex(int(s))) - 2
    except:
        temp_len = len(hex(int(float(s)))) - 2
    return temp_len + 1 if temp_len & 1 else temp_len

class simulator:
    def __init__(self):
        self.valid_data = 0
        self.sign_data = 0
        self.id_subs_valid = 0
        self.id_subs_sign = 0
        self.id_subs = 0
        self.total_input = 0
        self.addr = []
        self.cnt = []
        self.bytes2 = []
        self.transfer = True
        self.FT = {}
        self.TO = {}

    # read and analyse data in one file
    def analyse_all(self, fp):
        with open(fp, 'r') as f:
            temp = f.readlines()
        for item in temp:
            temp_l = item.split()
            if len(temp_l) == 4:
                if temp_l[1] == 'null':
                    continue
                if temp_l[3] != '0x' and self.transfer:
                    continue
                temp_common = (s2HexL(temp_l[2]) + len(temp_l[3]) - 2) / 2 + TX_NONCE + TX_GAS_A_PRICE
                self.total_input += (len(temp_l[3]) - 2) / 2
                self.valid_data += temp_common + 2 * TX_ADDR
                self.sign_data += temp_common + TX_ADDR + TX_SIGN
    
    def analyse_contract(self):
        all_call = 0
        for i in range(TRA_FROM, TRA_TO):
            with open(TRA_PREFIX + str(i), 'r') as f:
                temp = f.readlines()
            for item in temp:
                temp_l = item.split()
                if len(temp_l) == 4:
                    if temp_l[1] == 'null':
                        continue
                    if int(float(temp_l[2])) == 0 and temp_l[3] != '0x':
                        all_call += 1
        return all_call

    def traverse_file(self):
        for i in range(TRA_FROM, TRA_TO):
            self.analyse_all(TRA_PREFIX + str(i))
            #print("Traverse %s [ok] valid: %d | sign: %d" % (TRA_PREFIX + str(i), self.valid_data, self.sign_data))
        print("Traverse [ok] valid: %d | sign: %d" % (self.valid_data, self.sign_data))
        print("Total input: %d" % self.total_input)

    def output_data(self):
        with open(OUTPUT_FILE, 'w') as f:
            f.write("Total valid data: {}\n".format(str(self.valid_data)))
            f.write("Total sign data: {}\n".format(str(self.sign_data)))
            f.write("Total id subs valid: {}\n".format(str(self.id_subs_valid)))
            f.write("Total id subs sign: {}\n".format(str(self.id_subs_sign)))

    def get_tranfer(self):
        for i in range(TRA_FROM, TRA_TO):
            with open(TRA_PREFIX + str(i), 'r') as f:
                temp = f.readlines()
            for item in temp:
                temp_l = item.split()
                if len(temp_l) == 4:
                    if temp_l[3] != '0x':
                        continue
                    if temp_l[0] in self.FT:
                        self.FT[temp_l[0]] += 1
                    else:
                        self.FT[temp_l[0]] = 1
                    if temp_l[1] in self.FT:
                        self.FT[temp_l[1]] += 1
                    else:
                        self.FT[temp_l[1]] = 1
                    if temp_l[1] in self.TO:
                        self.TO[temp_l[1]] += 1
                    else:
                        self.TO[temp_l[1]] = 1
        
    def get_all(self):
        for i in range(TRA_FROM, TRA_TO):
            with open(TRA_PREFIX + str(i), 'r') as f:
                temp = f.readlines()
            for item in temp:
                temp_l = item.split()
                if len(temp_l) == 4:
                    if temp_l[0] in self.FT:
                        self.FT[temp_l[0]] += 1
                    else:
                        self.FT[temp_l[0]] = 1
                    if temp_l[1] in self.FT:
                        self.FT[temp_l[1]] += 1
                    else:
                        self.FT[temp_l[1]] = 1
                    if temp_l[1] in self.TO:
                        self.TO[temp_l[1]] += 1
                    else:
                        self.TO[temp_l[1]] = 1

    def output_FT_TO(self, ft, to):
        self.FT = sorted(self.FT.items(), key=lambda x: x[0])
        with open(ft, 'w') as f:
            for k in self.FT:
                f.write(k[0] + " " + str(k[1]) + "\n")
        self.TO = sorted(self.TO.items(), key=lambda x: x[0])
        with open(to, 'w') as f:
            for k in self.TO:
                f.write(k[0] + " " + str(k[1]) + "\n")

    def read_addr_data(self, db1 = True):
        db_prefix = DB1_PREFIX if db1 else DB2_PREFIX
        with open(db_prefix + '_' + str(DB_CUR), 'r') as f:
            temp = f.readlines()
        self.addr = list(map(lambda l: l.split()[0], temp))
        self.cnt = list(map(lambda l: int(l.split()[1]), temp))

    # compare two datasets, #1 last addrdb, #2 current addrdb
    def analyse_id(self, db1 = True):
        db_prefix = DB1_PREFIX if db1 else DB2_PREFIX
        th1 = ID_TO_TH1 if db1 else ID_FT_TH1
        th2 = ID_TO_TH2 if db1 else ID_FT_TH2
        th3 = ID_TO_TH3 if db1 else ID_FT_TH3
        with open(db_prefix + '_' + str(DB_CUR - 1), 'r') as f:
            last = f.readlines()
        temp_addr = list(map(lambda l: l.split()[0], last))
        temp_cnt = list(map(lambda l: int(l.split()[1]), last))
        del last
        cursor1 = 0
        cursor2 = 0
        limit1 = len(self.addr)
        limit2 = len(temp_addr)
        while cursor1 < limit1 and cursor2 < limit2:
            if self.addr[cursor1] > temp_addr[cursor2]:
                cursor2 += 1
            elif self.addr[cursor1] == temp_addr[cursor2]:
                if temp_cnt[cursor2] >= th1:
                    self.id_subs += ID1 * self.cnt[cursor1]
                elif temp_cnt[cursor2] >= th2:
                    self.id_subs += ID2 * self.cnt[cursor1]
                elif temp_cnt[cursor2] >= th3:
                    self.id_subs += ID3 * self.cnt[cursor1]
                else:
                    self.id_subs += ID4 * self.cnt[cursor1]
                cursor1 += 1
                cursor2 += 1
            else:
                cursor1 += 1
        if db1:
            self.id_subs_sign = self.id_subs
            print("id_subs_sign [ok] %d" % self.id_subs_sign)
        else:
            self.id_subs_valid = self.id_subs
            print("id_subs_valid [ok] %d" % self.id_subs_valid)
        del self.addr
        del self.cnt

if __name__ == "__main__":
    simu = simulator()
    flag_all = False
    flag_id = False
    flag_transfer = False
    flag_extractall = True
    if flag_all:
        simu.traverse_file()
        simu.output_data()
        #print(simu.analyse_contract())
    if flag_id:
        simu.read_addr_data()
        simu.analyse_id()
        simu.read_addr_data(False)
        simu.analyse_id(False)
        simu.output_data()
    if flag_transfer:
        out_ft = 'transfer_ft4'
        out_to = 'transfer_to4'
        simu.get_tranfer()
        simu.output_FT_TO(out_ft, out_to)
    if flag_extractall:
        out_ft = 'all_ft10'
        out_to = 'all_to10'
        simu.get_all()
        simu.output_FT_TO(out_ft, out_to)
