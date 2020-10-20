import matplotlib.pyplot as plt
import numpy as np

class Draw:
    def __init__(self, jump = False):
        plt.figure(figsize=(9, 5))
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.tick_params(labelsize=12)
        self.plot = plt.subplot(111)
        self.length = 0
        self.jump_zero = jump
        self.x = []
        self.y = []
        self.filename = ''
        self.datalimit = 1000000
    
    def set_fn(self, fn):
        self.filename = fn

    def init_draw(self):
        self.plot.set_xscale("log")
        font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 18,}
        plt.xlabel('Transfer Value (wei)', font)
        plt.ylabel('Occurence (times)', font)

    def read_data(self):
        with open(self.filename, 'r') as f:
            current = 0
            for line in f:
                if self.jump_zero:
                    self.jump_zero = False
                    continue
                if current == self.datalimit:
                    current = 0
                    self.draw_scatter()
                    self.x = []
                    self.y = []
                else:
                    templine = line.split()
                    self.x.append(int(templine[0]))
                    self.y.append(int(templine[1]))
                    current += 1
            if self.x:
                self.draw_scatter()
                self.x = []
                self.y = []

    def draw_scatter(self):
        self.plot.scatter(self.x, self.y, c = 'c', marker = '.')


if __name__ == "__main__":
    input_f = 'Amount_xy'
    d = Draw(True)
    d.set_fn(input_f)
    d.init_draw()
    d.read_data()
    plt.show()