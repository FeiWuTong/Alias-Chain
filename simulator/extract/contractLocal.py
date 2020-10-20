TRA_FROM = 501
TRA_TO = 1001
TRA_PREFIX = 'txStatis'

class cl:
    def __init__(self):
        self.data = []

    def set_contract(self, contract):
        self.contract = contract

    def trace(self):
        for i in range(TRA_FROM, TRA_TO):
            with open(TRA_PREFIX + str(i), 'r') as f:
                temp = f.readlines()
            for line in temp:
                item = line.split()
                if item[1] == self.contract:
                    if item[3] == '0x':
                        continue
                    self.data.append(item[3] + '\n')

    def output(self, fp):
        self.data.sort()
        with open(fp, 'w') as f:
            f.writelines(self.data)

if __name__ == "__main__":
    # test
    # 0xd0a6e6c54dbc68db5db3a091b171a77407ff7ccf 184202
    # 0x9e96604445ec19ffed9a5e8dd7b50a29c899a10c 8233
    # 0x12459c951127e0c374ff9105dda097662a027093 129230
    # 0xe5b9746dfcc2ef1054d47a451a77bb5f390c468d 65206

    # top 5 contracts in 5.5-6M blockheight
    # 0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208 2140220
    # 0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0 771308
    # 0x8d12a197cb00d4747a1fe03395095ce2a5cc6819 675663
    # 0x3495ffcee09012ab7d827abf3e3b3ae428a38443 568788
    # 0xf230b790e05390fc8295f4d3f60332c93bed42e2 483436
    contract = "0x3495ffcee09012ab7d827abf3e3b3ae428a38443"

    output_file = 'contract_top_4'
    mycl = cl()
    mycl.set_contract(contract)
    mycl.trace()
    mycl.output(output_file)