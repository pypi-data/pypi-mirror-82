import numpy as np


def get_score(para):
    return -(para["x1"] * para["x1"])


search_space = {
    "x1": np.arange(-100, 100, 1),
}


def _base_test(
    opt_class, n_iter, get_score=get_score, search_space=search_space, opt_para={},
):
    opt = opt_class(search_space, **opt_para)
    opt.search(get_score, n_iter=n_iter)

