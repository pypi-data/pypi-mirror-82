"""
    scorelator
    ~~~~~~~~~~
"""
import os
from typing import List, Tuple, Union
from pathlib import Path
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy.integrate import trapz
from mrtool import MRData, MRBRT, MRBeRT
from mrtool.core.other_sampling import sample_simple_lme_beta, extract_simple_lme_specs, extract_simple_lme_hessian


class Scorelator:
    """Evaluate the score of the result.
    Warning: This is specifically designed for the relative risk application.
    Haven't been tested for others.
    """
    def __init__(self,
                 ln_rr_draws: np.ndarray,
                 exposures: np.ndarray,
                 exposure_domain: Union[List[float], None] = None,
                 ref_exposure: Union[float, None] = None,
                 score_type: str = 'area'):
        """Constructor of Scorelator.

        Args:
            ln_rr_draws (np.ndarray):
                Draws for log relative risk, each row corresponds to one draw.
            exposures (np.ndarray):
                Exposures pair with the `ln_rr_draws`, its size should match
                the number of columns of `ln_rr_draws`.
            exposure_domain (Union[List[float], None], optional):
                The exposure domain that will be considered for the score evaluation.
                If `None`, consider the whole domain defined by `exposure`.
                Default to None.
            ref_exposure (Union[float, None], optional):
                Reference exposure, the `ln_rr_draws` will be normalized to this point.
                All draws in `ln_rr_draws` will have value 0 at `ref_exposure`.
                If `None`, `ref_exposure` will be set to the minimum value of `exposures`.
                Default to None.
            score_type (str, optional):
                If ``'area'``, use area between curves to determine the score, if ``'point'``,
                use the ratio between line segments at point exposure to determine the score.
        """
        self.ln_rr_draws = np.array(ln_rr_draws)
        self.exposures = np.array(exposures)
        self.exposure_domain = [np.min(self.exposures),
                                np.max(self.exposures)] if exposure_domain is None else exposure_domain
        self.ref_exposure = np.min(self.exposures) if ref_exposure is None else ref_exposure

        self.num_draws = self.ln_rr_draws.shape[0]
        self.num_exposures = self.exposures.size

        # normalize the ln_rr_draws
        if self.ln_rr_draws.shape[1] > 1:
            self.ln_rr_draws = self.normalize_ln_rr_draws()
        self.rr_draws = np.exp(self.ln_rr_draws)
        self.rr_type = 'harmful' if self.rr_draws[:, -1].mean() >= 1.0 else 'protective'

        self.score_type = score_type
        self._check_inputs()

    def _check_inputs(self):
        """Check the inputs type and value.
        """
        if self.exposures.size != self.ln_rr_draws.shape[1]:
            raise ValueError(f"Size of the exposures ({self.exposures.size}) should be consistent"
                             f"with number of columns of ln_rr_draws ({self.ln_rr_draws.shape[1]})")

        if self.exposure_domain[0] > self.exposure_domain[1]:
            raise ValueError(f"Lower bound of exposure_domain ({self.exposure_domain[0]}) should be"
                             f"less or equal than upper bound ({self.exposure_domain[1]})")

        if not any((self.exposures >= self.exposure_domain[0]) &
                   (self.exposures <= self.exposure_domain[1])):
            raise ValueError("No exposures in the exposure domain.")

        if self.ref_exposure < np.min(self.exposures) or self.ref_exposure > np.max(self.exposures):
            raise ValueError("reference exposure should be within the range of exposures.")

        if not self.score_type in ['area', 'point']:
            raise ValueError("score_type has to been chosen from 'area' or 'point'.")

    def normalize_ln_rr_draws(self):
        """Normalize log relative risk draws.
        """
        shift = np.array([
            np.interp(self.ref_exposure, self.exposures, ln_rr_draw)
            for ln_rr_draw in self.ln_rr_draws
        ])
        return self.ln_rr_draws - shift[:, None]

    def get_evidence_score(self,
                           lower_draw_quantile: float = 0.025,
                           upper_draw_quantile: float = 0.975,
                           path_to_diagnostic: Union[str, Path, None] = None) -> float:
        """Get evidence score.

        Args:
            lower_draw_quantile (float, optional): Lower quantile of the draw for the score.
            upper_draw_quantile (float, optioanl): Upper quantile of the draw for the score.
            path_to_diagnostic (Union[str, Path, None], optional):
                Path of where the picture is saved, if None the plot will not be saved.
                Default to None.

        Returns:
            float: Evidence score.
        """
        rr_mean = np.median(self.rr_draws, axis=0)
        rr_lower = np.quantile(self.rr_draws, lower_draw_quantile, axis=0)
        rr_upper = np.quantile(self.rr_draws, upper_draw_quantile, axis=0)

        valid_index = (self.exposures >= self.exposure_domain[0]) & (self.exposures <= self.exposure_domain[1])

        if self.score_type == 'area':
            ab = seq_area_between_curves(rr_lower, rr_upper)
        else:
            ab = rr_upper - rr_lower
        if self.rr_type == 'protective':
            if self.score_type == 'area':
                abc = seq_area_between_curves(rr_lower, np.ones(self.num_exposures))
            else:
                abc = 1.0 - rr_lower
        elif self.rr_type == 'harmful':
            if self.score_type == 'area':
                abc = seq_area_between_curves(np.ones(self.num_exposures), rr_upper)
            else:
                abc = rr_upper - 1.0
        else:
            raise ValueError('Unknown relative risk type.')
        score = np.round((ab/abc)[valid_index].min(), 2)

        # plot diagnostic
        if path_to_diagnostic is not None:
            fig, ax = plt.subplots(1, 2, figsize=(22, 8.5))
            # plot rr uncertainty
            if self.exposures.size == 1:
                ax[0].boxplot(self.rr_draws,
                              meanline=True,
                              whis=(lower_draw_quantile*100, upper_draw_quantile*100),
                              positions=self.exposures)
            else:
                ax[0].fill_between(self.exposures, rr_lower, rr_upper, color='#69b3a2', alpha=0.3)
                ax[0].plot(self.exposures, rr_mean, color='#69b3a2')
                ax[0].set_xlim(np.min(self.exposures), np.max(self.exposures))
                ax[0].set_ylim(np.min(rr_lower) - rr_mean.ptp()*0.1, np.max(rr_upper) + rr_mean.ptp()*0.1)
            ax[0].axhline(1, color='#003333', alpha=0.5)
            # compute coordinate of annotation of A, B and C
            if self.rr_type == 'protective':
                self.annotate_between_curve('A', self.exposures, rr_lower, rr_mean, ax[0])
                self.annotate_between_curve('B', self.exposures, rr_mean, rr_upper, ax[0])
                self.annotate_between_curve('C', self.exposures, rr_upper, np.ones(self.num_exposures),
                                            ax[0], mark_area=True)
            else:
                self.annotate_between_curve('A', self.exposures, rr_mean, rr_upper, ax[0])
                self.annotate_between_curve('B', self.exposures, rr_lower, rr_mean, ax[0])
                self.annotate_between_curve('C', self.exposures, np.ones(self.num_exposures), rr_lower,
                                            ax[0], mark_area=True)

            # plot the score as function of exposure
            if self.exposures.size == 1:
                ax[1].scatter(self.exposures, ab/abc,
                              color='dodgerblue',
                              label=f'A+B / A+B+C: {score}')
            else:
                ax[1].plot(self.exposures, ab/abc,
                           color='dodgerblue',
                           label=f'A+B / A+B+C: {score}')
                ax[1].set_xlim(np.min(self.exposures), np.max(self.exposures))
            ax[1].legend()
            ax[1].legend(loc=1, fontsize='x-large')

            # plot the exposure domain
            ax[0].axvline(self.exposure_domain[0], linestyle='--', color='#003333')
            ax[0].axvline(self.exposure_domain[1], linestyle='--', color='#003333')
            ax[1].axvline(self.exposure_domain[0], linestyle='--', color='#003333')
            ax[1].axvline(self.exposure_domain[1], linestyle='--', color='#003333')

            plt.savefig(path_to_diagnostic, bbox_inches='tight')

        return score

    @staticmethod
    def annotate_between_curve(annotation: str,
                               x: np.ndarray, y_lower: np.ndarray, y_upper: np.ndarray, ax: Axes,
                               mark_area: bool = False):
        """Annotate between the curve.

        Args:
            annotation (str): the annotation between the curve.
            x (np.ndarray): independent variable.
            y_lower (np.ndarray): lower bound of the curve.
            y_upper (np.ndarray): upper bound of the curve.
            ax (Axes): axis of the plot.
            mark_area (bool, optional): If True mark the area. Default to False.
        """
        y_diff = y_upper - y_lower
        label_index = np.argmax(y_diff)
        if label_index > 0.95*len(x) or label_index < 0.05*len(x):
            label_index = int(0.4*len(x))
        label_x = x[label_index]
        label_y = 0.5*(y_lower[label_index] + y_upper[label_index])
        if label_y < y_upper[label_index]:
            ax.text(label_x, label_y, annotation, color='dodgerblue',
                    horizontalalignment='center', verticalalignment='center', size=20)

        if mark_area:
            ax.fill_between(x, y_lower, y_upper, linestyle='--', where=y_lower < y_upper,
                            edgecolor='black', facecolor="none", alpha=0.5)



def area_between_curves(lower: np.ndarray,
                        upper: np.ndarray,
                        ind_var: Union[np.ndarray, None] = None,
                        normalize_domain: bool = True) -> float:
    """Compute area between curves.

    Args:
        lower (np.ndarray): Lower bound curve.
        upper (np.ndarray): Upper bound curve.
        ind_var (Union[np.ndarray, None], optional):
            Independent variable, if `None`, it will assume sample points are
            evenly spaced. Default to None.
        normalize_domain (bool, optional):
            If `True`, when `ind_var` is `None`, will normalize domain to 0 and 1.
            Default to True.

    Returns:
        float: Area between curves.
    """
    assert upper.size == lower.size, "Vectors for lower and upper curve should have same size."
    if ind_var is not None:
        assert ind_var.size == lower.size, "Independent variable size should be consistent with the curve vector."
    assert lower.size >= 2, "At least need to have two points to compute interval."

    diff = upper - lower
    if ind_var is not None:
        return trapz(diff, x=ind_var)
    else:
        if normalize_domain:
            dx = 1.0/(diff.size - 1)
        else:
            dx = 1.0
        return trapz(diff, dx=dx)


def seq_area_between_curves(lower: np.ndarray,
                            upper: np.ndarray,
                            ind_var: Union[np.ndarray, None] = None,
                            normalize_domain: bool = True) -> np.ndarray:
    """Sequence areas_between_curves.

    Args: Please check the inputs for area_between_curves.

    Returns:
        np.ndarray:
            Return areas defined from the first two points of the curve
            to the whole curve.
    """
    if ind_var is None:
        area = np.array([area_between_curves(
            lower[:(i+1)],
            upper[:(i+1)],
            normalize_domain=normalize_domain)
            for i in range(1, lower.size)
        ])
    else:
        area = np.array([area_between_curves(
            lower[:(i + 1)],
            upper[:(i + 1)],
            ind_var[:(i + 1)],
            normalize_domain=normalize_domain)
            for i in range(1, lower.size)
        ])
    return np.hstack((area[0], area))


class ContinuousScorelator:
    def __init__(self,
                 signal_model: Union[MRBRT, MRBeRT],
                 final_model: Union[MRBRT],
                 alt_cov_names: List[str],
                 ref_cov_names: List[str],
                 exposure_bounds: Tuple[float] = (0.15, 0.85),
                 draw_bounds: Tuple[float] = (0.05, 0.95),
                 num_samples: int = 1000,
                 num_points: int = 100,
                 shift_draws_by_min: bool = False,
                 name: str = 'unknown'):
        self.signal_model = signal_model
        self.final_model = final_model
        self.alt_cov_names = alt_cov_names
        self.ref_cov_names = ref_cov_names
        self.exposure_bounds = exposure_bounds
        self.draw_bounds = draw_bounds
        self.num_samples = num_samples
        self.num_points = num_points
        self.shift_draws_by_min = shift_draws_by_min
        self.name = name

        exposures = self.signal_model.data.get_covs(self.alt_cov_names + self.ref_cov_names)
        self.exposure_lend = exposures.min()
        self.exposure_uend = exposures.max()
        self.alt_exposures = self.signal_model.data.get_covs(self.alt_cov_names).mean(axis=1)
        self.ref_exposures = self.signal_model.data.get_covs(self.ref_cov_names).mean(axis=1)
        self.draws = self.get_draws(num_samples=self.num_samples, num_points=self.num_points)
        self.wider_draws = self.get_draws(num_samples=self.num_samples, num_points=self.num_points,
                                          use_gamma_ub=True)
        self.pred_exposures = self.get_pred_exposures()
        self.pred = self.get_pred()

        if self.shift_draws_by_min:
            index = np.argmin(self.pred)
            self.draws -= self.draws[:, index, None]
            self.wider_draws -= self.wider_draws[:, index, None]

        # compute the range of exposures
        self.exposure_lb = np.quantile(self.ref_exposures, self.exposure_bounds[0])
        self.exposure_ub = np.quantile(self.alt_exposures, self.exposure_bounds[1])
        self.effective_index = (self.pred_exposures >= self.exposure_lb) & (self.pred_exposures <= self.exposure_ub)

        # compute the range of the draws
        self.draw_lb = np.quantile(self.draws, self.draw_bounds[0], axis=0)
        self.draw_ub = np.quantile(self.draws, self.draw_bounds[1], axis=0)
        self.wider_draw_lb = np.quantile(self.wider_draws, self.draw_bounds[0], axis=0)
        self.wider_draw_ub = np.quantile(self.wider_draws, self.draw_bounds[1], axis=0)

    def get_signal(self,
                   alt_cov: List[np.ndarray],
                   ref_cov: List[np.ndarray]) -> np.ndarray:
        covs = {}
        for i, cov_name in enumerate(self.alt_cov_names):
            covs[cov_name] = alt_cov[i]
        for i, cov_name in enumerate(self.ref_cov_names):
            covs[cov_name] = ref_cov[i]
        data = MRData(covs=covs)
        return self.signal_model.predict(data)

    def get_pred_exposures(self, num_points: int = 100):
        return np.linspace(self.exposure_lend, self.exposure_uend, num_points)

    def get_pred_data(self, num_points: int = 100) -> MRData:
        exposures = self.get_pred_exposures(num_points=num_points)
        ref_cov = np.repeat(self.exposure_lend, num_points)
        zero_cov = np.zeros(num_points)
        signal = self.get_signal(
            alt_cov=[exposures for _ in self.alt_cov_names],
            ref_cov=[ref_cov for _ in self.ref_cov_names]
        )
        other_covs = {
            cov_name: zero_cov
            for cov_name in self.final_model.data.covs
            if cov_name != 'signal'
        }
        return MRData(covs={'signal': signal, **other_covs})

    def get_beta_samples(self, num_samples: int) -> np.ndarray:
        return sample_simple_lme_beta(num_samples, self.final_model)

    def get_gamma_samples(self, num_samples: int) -> np.ndarray:
        return np.repeat(self.final_model.gamma_soln.reshape(1, 1),
                         num_samples, axis=0)

    def get_samples(self, num_samples: int) -> Tuple[np.ndarray, np.ndarray]:
        return self.get_beta_samples(num_samples), self.get_gamma_samples(num_samples)

    def get_gamma_sd(self) -> float:
        lt = self.final_model.lt
        gamma_fisher = lt.get_gamma_fisher(lt.gamma)
        return 1.0/np.sqrt(gamma_fisher[0, 0])

    def get_draws(self,
                  num_samples: int = 1000,
                  num_points: int = 100,
                  use_gamma_ub: bool = False) -> np.ndarray:
        data = self.get_pred_data(num_points=num_points)
        beta_samples, gamma_samples = self.get_samples(num_samples=num_samples)
        if use_gamma_ub:
            gamma_samples += 2.0*self.get_gamma_sd()
        return self.final_model.create_draws(data,
                                             beta_samples=beta_samples,
                                             gamma_samples=gamma_samples,
                                             random_study=True).T

    def is_harmful(self) -> bool:
        median = np.median(self.draws, axis=0)
        return np.sum(median[self.effective_index] >= 0) > 0.5*np.sum(self.effective_index)

    def get_pred(self) -> np.ndarray:
        ref_cov = np.repeat(self.exposure_lend, self.num_points)
        zero_cov = np.zeros(self.num_points)
        signal = self.get_signal(
            alt_cov=[self.pred_exposures for _ in self.alt_cov_names],
            ref_cov=[ref_cov for _ in self.ref_cov_names]
        )
        other_covs = {
            cov_name: zero_cov
            for cov_name in self.final_model.data.covs
            if cov_name != 'signal'
        }
        return self.final_model.predict(MRData(covs={'signal': signal, **other_covs}))


    def get_score(self, use_gamma_ub: bool = False) -> float:
        if self.is_harmful():
            draw = self.wider_draw_lb if use_gamma_ub else self.draw_lb
            score = draw[self.effective_index].mean()
        else:
            draw = self.wider_draw_ub if use_gamma_ub else self.draw_ub
            score = -draw[self.effective_index].mean()
        return score

    def plot_data(self, ax=None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot()
        data = self.signal_model.data
        alt_exposure = data.get_covs(self.alt_cov_names)
        ref_exposure = data.get_covs(self.ref_cov_names)

        alt_mean = alt_exposure.mean(axis=1)
        ref_mean = ref_exposure.mean(axis=1)
        ref_cov = np.repeat(self.exposure_lend, data.num_obs)
        zero_cov = np.zeros(data.num_obs)
        signal = self.get_signal(
            alt_cov=[ref_mean for _ in self.alt_cov_names],
            ref_cov=[ref_cov for _ in self.ref_cov_names]
        )
        other_covs = {
            cov_name: zero_cov
            for cov_name in self.final_model.data.covs
            if cov_name != 'signal'
        }
        prediction = self.final_model.predict(MRData(covs={'signal': signal, **other_covs}))
        if self.shift_draws_by_min:
            prediction -= np.min(self.pred)
        if isinstance(self.signal_model, MRBRT):
            w = self.signal_model.w_soln
        else:
            w = np.vstack([model.w_soln for model in self.signal_model.sub_models]).T.dot(self.signal_model.weights)
        trim_index = w <= 0.1
        ax.scatter(alt_mean, prediction + data.obs,
                   c='gray', s=5.0/data.obs_se, alpha=0.5)
        ax.scatter(alt_mean[trim_index], prediction[trim_index] + data.obs[trim_index],
                   c='red', marker='x', s=5.0/data.obs_se[trim_index])

    def plot_model(self,
                   ax=None,
                   title: str = None,
                   xlabel: str = 'exposure',
                   ylabel: str = 'ln relative risk',
                   xlim: tuple = None,
                   ylim: tuple = None,
                   xscale: str = None,
                   yscale: str = None,
                   folder: Union[str, Path] = None):

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot()
        draws_median = np.median(self.draws, axis=0)

        ax.plot(self.pred_exposures, draws_median, color='#69b3a2', linewidth=1)
        ax.fill_between(self.pred_exposures, self.draw_lb, self.draw_ub, color='#69b3a2', alpha=0.2)
        ax.fill_between(self.pred_exposures, self.wider_draw_lb, self.wider_draw_ub, color='#69b3a2', alpha=0.2)
        ax.axvline(self.exposure_lb, linestyle='--', color='k', linewidth=1)
        ax.axvline(self.exposure_ub, linestyle='--', color='k', linewidth=1)
        ax.axhline(0.0, linestyle='--', color='k', linewidth=1)

        title = self.name if title is None else title
        score = self.get_score()
        low_score = self.get_score(use_gamma_ub=True)
        title = f"{title}: score = ({low_score: .3f}, {score: .3f})"

        ax.set_title(title, loc='left')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if xlim is not None:
            ax.set_xlim(*xlim)
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xscale is not None:
            ax.set_xscale(xscale)
        if yscale is not None:
            ax.set_yscale(yscale)

        self.plot_data(ax=ax)

        if folder is not None:
            folder = Path(folder)
            if not folder.exists():
                os.mkdir(folder)
            plt.savefig(folder/f"{self.name}.pdf", bbox_inches='tight')

        return ax

class DichotomousScorelator:
    def __init__(self,
                 model: MRBRT,
                 cov_name: str = 'intercept',
                 draw_bounds: Tuple[float, float] = (0.05, 0.95),
                 name: str = 'unknown'):
        self.model = model
        self.cov_name = cov_name
        self.draw_bounds = draw_bounds
        self.cov_index = self.model.get_cov_model_index(self.cov_name)
        self.name = name

        x_ids = self.model.x_vars_indices[self.cov_index]
        z_ids = self.model.z_vars_indices[self.cov_index]
        self.beta = self.model.beta_soln[x_ids][0]
        self.gamma = self.model.gamma_soln[z_ids][0]

        # compute the fixed effects uncertainty
        model_specs = extract_simple_lme_specs(self.model)
        beta_var = np.linalg.inv(extract_simple_lme_hessian(model_specs))
        self.beta_var = beta_var[np.ix_(x_ids, x_ids)][0, 0]

        # compute the random effects uncertainty
        lt = self.model.lt
        gamma_fisher = lt.get_gamma_fisher(lt.gamma)
        gamma_var = np.linalg.inv(gamma_fisher)
        self.gamma_var = gamma_var[np.ix_(z_ids, z_ids)][0, 0]

        # compute score
        gamma_ub = self.gamma + 2.0*np.sqrt(self.gamma_var)
        self.draw_lb = self.beta + norm.ppf(self.draw_bounds[0], scale=np.sqrt(self.gamma + self.beta_var))
        self.draw_ub = self.beta + norm.ppf(self.draw_bounds[1], scale=np.sqrt(self.gamma + self.beta_var))
        self.wider_draw_lb = self.beta + norm.ppf(self.draw_bounds[0], scale=np.sqrt(gamma_ub + self.beta_var))
        self.wider_draw_ub = self.beta + norm.ppf(self.draw_bounds[1], scale=np.sqrt(gamma_ub + self.beta_var))

    def get_score(self, use_gamma_ub: bool = False) -> float:
        if use_gamma_ub:
            score = self.wider_draw_lb
        else:
            score = self.draw_lb
        return score

    def plot_model(self,
                   ax=None,
                   title: str = None,
                   xlabel: str = 'ln relative risk',
                   ylabel: str = 'ln relative risk se',
                   xlim: tuple = None,
                   ylim: tuple = None,
                   xscale: str = None,
                   yscale: str = None,
                   folder: Union[str, Path] = None):
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot()
        data = self.model.data
        trim_index = self.model.w_soln <= 0.1
        max_obs_se = np.max(data.obs_se)*1.1
        ax.set_ylim(max_obs_se, 0.0)
        ax.fill_betweenx([0.0, max_obs_se],
                         [self.beta, self.beta - max_obs_se],
                         [self.beta, self.beta + max_obs_se], color='#B0E0E6', alpha=0.4)
        ax.scatter(data.obs, data.obs_se, color='gray', alpha=0.4)
        ax.scatter(data.obs[trim_index],
                   data.obs_se[trim_index], color='red', marker='x', alpha=0.4)
        ax.plot([self.beta, self.beta - max_obs_se], [0.0, max_obs_se],
                linewidth=1, color='#87CEFA')
        ax.plot([self.beta, self.beta + max_obs_se], [0.0, max_obs_se],
                linewidth=1, color='#87CEFA')

        ax.axvline(0.0, color='r', linewidth=1, linestyle='--')
        ax.axvline(self.beta, color='k', linewidth=1, linestyle='--')
        ax.axvline(self.draw_lb, color='#69b3a2', linewidth=1)
        ax.axvline(self.draw_ub, color='#69b3a2', linewidth=1)
        ax.axvline(self.wider_draw_lb, color='#256b5f', linewidth=1)
        ax.axvline(self.wider_draw_ub, color='#256b5f', linewidth=1)

        title = self.name if title is None else title
        score = self.get_score()
        low_score = self.get_score(use_gamma_ub=True)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{title}: score = ({low_score: .3f}, {score: .3f})", loc='left')

        if xlim is not None:
            ax.set_xlim(*xlim)
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xscale is not None:
            ax.set_xscale(xscale)
        if yscale is not None:
            ax.set_yscale(yscale)

        if folder is not None:
            folder = Path(folder)
            if not folder.exists():
                os.mkdir(folder)
            plt.savefig(folder/f"{self.name}.pdf", bbox_inches='tight')

        return ax