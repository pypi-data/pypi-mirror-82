import copy
from typing import Tuple, List, Sequence, Union, Dict, Callable

import numpy as np
from scipy.optimize import minimize, OptimizeResult

from vanilla_option_pricing.option import VanillaOption
from vanilla_option_pricing.option_pricing import OptionPricingModel


class ModelCalibration:
    """
    Calibrate option pricing models with prices of listed options

    :param options: a collection of :class:`~option.VanillaOption`
    """

    DEFAULT_PARAMETER_LOWER_BOUND = 1e-4

    def __init__(self, options: List[VanillaOption]):
        self.options = options

    def calibrate_model(
            self,
            model: OptionPricingModel,
            method: str = None,
            options: Dict = None,
            bounds: Union[str, Sequence[Tuple[float, float]]] = 'default'
    ) -> Tuple[OptimizeResult, OptionPricingModel]:
        """
        Tune model parameters and returns a tuned model. The algorithm tries to minimize the squared difference
        between the prices of listed options and the prices predicted by the model: the parameters of the model
        are the optimization variables.
        The numerical optimization is performed by :func:`~scipy.optimize.minimize` in the scipy package.

        :param model: the model to calibrate
        :param method: see :func:`~scipy.optimize.minimize`
        :param options: see :func:`~scipy.optimize.minimize`
        :param bounds: the bounds to apply to parameters. If none is specified, then the
                       :attr:`~DEFAULT_PARAMETER_LOWER_BOUND` is applied for all the parameters.
                       Otherwise, a list of tuples (lower_bound, upper_bound) for each parameter shall be specified.
        :return: a tuple (res, model), where res is the result of :func:`~scipy.optimize.minimize`,
                 while model a calibrated model
        """
        if bounds == 'default':
            bounds = ((self.DEFAULT_PARAMETER_LOWER_BOUND, None),) * len(model.parameters)
        new_model = copy.deepcopy(model)
        loss = self._get_loss_function(new_model)
        res = minimize(loss, np.array(new_model.parameters), bounds=bounds, method=method, options=options)
        new_model.parameters = res.x
        return res, new_model

    def _get_loss_function(self, model: OptionPricingModel) -> Callable[[Sequence[float]], float]:
        def _loss_function(parameters: Sequence[float]) -> float:
            model.parameters = parameters
            predicted_prices = np.array([model.price_option_black(o) for o in self.options])
            real_prices = np.array([o.price for o in self.options])
            return ((predicted_prices - real_prices) ** 2).sum()

        return _loss_function
