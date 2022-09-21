import numpy as np
import matplotlib.pyplot as plt

# Diablo III Grand Rift Exp Efficiency Graph


class Diablo3GrExpGraph(object):

    def __init__(self, baseLevel=85, extremeLvl=125):

        self.baseLvl = baseLevel
        self.baseData = self.genData()

    def genData(self) -> list:
        data1 = [[l, 90] for l in range(1, self.baseLvl + 1)]
        data2 = [
            [85, 90],
            [90, 105],
            [95, 120],
            [100, 150],
            [105, 150],
            [107, 155],
            [108, 200],
            [110, 210],
            [113, 250],
            [114, 270],
            [115, 330],
            [118, 400],
            [124, 900],
        ]
        data = data1+data2
        return data

    def draw(self):
        ...


    def test(self):
        # x = np.arange(baseLvl, 150, 1)
        x = np.array(self.baseData)
        y1 = np.power(1.05, x - self.baseLvl) * 10000
        # y2 = np.power(1.0565, x-baseLvl)+0.5
        y2 = (np.power(1.17, x - self.baseLvl) + 0.5) * 10000

        static_cost_of_time = 1.2  # 钥匙开销时间
        # y3 = np.power(1.05, x - self.baseLvl) / (np.power(1.0565, x - self.baseLvl) + static_cost_of_time)
        y3 = np.power(1.05, x - self.baseLvl) / (np.power(1.17, x - self.baseLvl) + static_cost_of_time) * 10000

        plt.plot(x, y1, color='red', label='exp')
        plt.plot(x, y2, color='green', label='time')
        plt.plot(x, y3, color='blue', label='final')
        # plt.plot(x, y3, color = 'blue', label = 'final', linestyle='--')

        plt.xlabel('GR-Tire')
        plt.ylabel('DiffIndex')

        plt.show()

if __name__ == "__main__":
    test = Diablo3GrExpGraph()
    test.test()
