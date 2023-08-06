# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import numpy as np
from scipy.stats import norm
from scipy.spatial.distance import cdist


from .sbom import SBOM


class ExpectedImprovementBasedOptimization(SBOM):
    def __init__(self, search_space, xi=0.01, **kwargs):
        super().__init__(search_space)
        self.new_positions = []
        self.xi = xi

    def _expected_improvement(self):
        all_pos_comb_sampled = self.get_random_sample()

        mu, sigma = self.regr.predict(all_pos_comb_sampled, return_std=True)
        mu_sample = self.regr.predict(self.X_sample)

        mu = mu.reshape(-1, 1)
        sigma = sigma.reshape(-1, 1)
        mu_sample = mu_sample.reshape(-1, 1)

        mu_sample_opt = np.max(mu_sample)
        imp = mu - mu_sample_opt - self.xi

        Z = np.divide(imp, sigma, out=np.zeros_like(sigma), where=sigma != 0)
        exp_imp = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
        exp_imp[sigma == 0.0] = 0.0

        return exp_imp

    def _propose_location(self):
        self.regr.fit(self.X_sample, self.Y_sample)

        exp_imp = self._expected_improvement()
        exp_imp = exp_imp[:, 0]

        index_best = list(exp_imp.argsort()[::-1])
        all_pos_comb_sorted = self.all_pos_comb[index_best]

        pos_best = [all_pos_comb_sorted[0]]

        while len(pos_best) < self.skip_retrain(len(self.pos_new)):
            if all_pos_comb_sorted.shape[0] == 0:
                break

            dists = cdist(
                all_pos_comb_sorted, [pos_best[-1]], metric="cityblock"
            )
            dists_norm = dists / dists.max()
            bool = np.squeeze(dists_norm > 0.25)
            all_pos_comb_sorted = all_pos_comb_sorted[bool]

            if len(all_pos_comb_sorted) > 0:
                pos_best.append(all_pos_comb_sorted[0])

        return pos_best

    @SBOM.track_X_sample
    def iterate(self):
        if len(self.new_positions) == 0:
            self.new_positions = self._propose_location()

        pos = self.new_positions[0]
        self.pos_new = pos

        self.new_positions.pop(0)
        self.pos = pos

        return pos

    def evaluate(self, score_new):
        self.score_new = score_new

        self._evaluate_new2current(score_new)
        self._evaluate_current2best()

        self.Y_sample.append(score_new)
