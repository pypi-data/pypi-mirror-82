"""
An example of using POSS to optimize a subset selection problem.
"""

from sparse_mse import SparseMSE
from zoopt import Objective, Parameter, ExpOpt
from math import exp

if __name__ == '__main__':
    # load data file
    mse = SparseMSE('sonar.arff')
    mse.set_sparsity(8)

    # setup objective
    # print(mse.get_dim().get_size())
    objective = Objective(func=mse.loss, dim=mse.get_dim(), constraint=mse.constraint)
    parameter = Parameter(algorithm='poss', budget=2 * exp(1) * (mse.get_sparsity() ** 2) * mse.get_dim().get_size(), seed=1)

    # perform sparse regression with constraint |w|_0 <= k
    solution_list = ExpOpt.min(objective, parameter, repeat=2, plot=False)
