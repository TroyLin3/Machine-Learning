"""
- Author: Haoxin Lin
- Email: linhx36@outlook.com
- Date: 2020.09.20
- Brief: Logit Regression
"""

import numpy as np
import matplotlib.pyplot as plt

class LogitReg:
    """ Logistic Regression """

    def __init__(self, xsize):
        """ Init parameters of the learner """
        # xsize: size of input
        self.xsize = xsize
        self.w = np.random.randn(self.xsize)
        self.b = np.random.randn()
        self.lr = 0.1      # learning rate

    def reset(self):
        """ Reset parameters """
        self.w = np.random.randn(self.xsize)
        self.b = np.random.randn()
        self.lr = 0.1
        del self.xs, self.ys

    def load(self, xs, ys):
        """ load dataset """
        # xs: x data
        # ys: y data
        self.xs = xs
        self.ys = ys

    def loss(self):
        """ Calculate Loss """
        ls = 0
        for i in range(self.xs.shape[0]):
            y = self.w.dot(self.xs[i]) + self.b    # output
            ls += np.log(1+np.exp(y)) - self.ys[i]*y
        ls /= self.xs.shape[0]
        return ls

    def learn(self):
        """ Learn nearly optimal parameters from data """
        print("### Start learning ###")
        print("Initial loss: %.4f"%self.loss())

        for step in range(20000):
            # 1st, 2st gradient of loss
            onegrad2w, twograd2w = np.zeros(self.w.shape), 0
            onegrad2b, twograd2b = 0, 0

            # gradient descent
            for i in range(self.xs.shape[0]):
                y = self.w.dot(self.xs[i]) + self.b    # output
                if y < 0:
                    p1 = np.exp(y)/(1+np.exp(y))      # likelihood func of y = 1
                else:
                    p1 = 1/(1+np.exp(-y))
                onegrad2w += self.xs[i]*(p1-self.ys[i])
                onegrad2b += p1 - self.ys[i]
                twograd2w += self.xs[i].dot(self.xs[i])*p1*(1-p1)
                twograd2b += p1*(1-p1)
            if twograd2w != 0:
                self.w -= self.lr*onegrad2w/twograd2w
            else:
                self.w = np.random.randn(self.xsize)
            if twograd2b != 0:
                self.b -= self.lr*onegrad2b/twograd2b
            else:
                self.b = np.random.randn()

            # new loss
            if step % 1000 == 0:
                print("Step %d: loss=%.4f"%(step+1, self.loss()))

    def predict(self, input):
        """ Predict new input """
        y = self.w.dot(input) + self.b
        return 1 if y > 0 else 0

    def visualize(self):
        """ Visualize data and parameters (Only for 3.3)"""
        plt.xlabel("x[0]: Density")
        plt.ylabel("x[1]: Sugar Content")
        positive_xs = self.xs[self.ys==1]
        negative_xs = self.xs[self.ys==0]

        # plot data
        plt.scatter(positive_xs[:, 0], positive_xs[:, 1], c='#00CED1', marker='+', s=80, label='Great (positive)')
        plt.scatter(negative_xs[:, 0], negative_xs[:, 1], c='#DC143C', marker='1', s=80, label='Awful (negative)')

        # plot partition
        x0 = np.arange(0, 1, 0.01)
        x1 = -(self.w[0]*x0+self.b)/self.w[1]
        plt.plot(x0, x1, c='m', label='Partition')

        plt.legend()
        plt.show()

    def test(self, xs, ys):
        """ Test on test dataset """
        ls = 0      # loss
        error_num = 0
        for i in range(xs.shape[0]):
            y = self.w.dot(xs[i]) + self.b    # output
            ls += np.log(1+np.exp(y)) - ys[i]*y
            if self.predict(xs[i]) != ys[i]:
                error_num += 1
        ls /= xs.shape[0]
        error_rate = error_num/xs.shape[0]
        return ls, error_rate