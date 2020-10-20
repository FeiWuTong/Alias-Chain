class Compare:
    def __init__(self):
        self.total = 0
        self.bingo = 0
    
    def run(self, fp1, fp2):
        with open(fp1, 'r') as f:
            temp1 = f.readlines()
        with open(fp2, 'r') as f:
            temp2 = f.readlines()
        i = j = 0
        n1 = len(temp1)
        self.total = n1
        n2 = len(temp2)
        while i < n1 and j < n2:
            if temp1[i] > temp2[j]:
                j += 1
            elif temp1[i] == temp2[j]:
                self.bingo += 1
                i += 1
                j += 1
            else:
                i += 1
        print("Total: %d" % self.total)
        print("Bingo: %d" % self.bingo)

if __name__ == "__main__":
    fp1 = 'to_87_3'
    fp2 = 'to_87_4'
    com = Compare()
    com.run(fp1, fp2)