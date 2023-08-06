# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np

from gradient_free_optimizers import BayesianOptimizer
from ._base_test import _base_test

n_iter = 33
opt = BayesianOptimizer


def get_score(para):
    return -(para["x1"] * para["x1"])


def test_skip_retrain():
    for skip_retrain in ["many", "some", "few", "never"]:
        opt_para = {"skip_retrain": skip_retrain}
        _base_test(opt, n_iter, opt_para=opt_para)


def test_warm_start_smbo():
    gpr_X, gpr_y = [], []
    for _ in range(10):
        pos_ = np.random.randint(0, high=9)
        pos = np.array([pos_])

        para = {
            "x1": pos_,
        }
        gpr_X.append(pos)
        gpr_y.append(get_score(para))

    for warm_start_smbo in [None, (gpr_X, gpr_y)]:
        opt_para = {"warm_start_smbo": warm_start_smbo}
        _base_test(opt, n_iter, opt_para=opt_para)


def test_max_sample_size():
    for max_sample_size in [10, 100, 10000, 10000000000]:
        opt_para = {"max_sample_size": max_sample_size}
        _base_test(opt, n_iter, opt_para=opt_para)
