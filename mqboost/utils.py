from itertools import chain, repeat
from typing import List

import numpy as np
import pandas as pd

from mqboost.base import AlphaLike, ValidationException, XdataLike, YdataLike


def alpha_validate(
    alphas: AlphaLike,
) -> List[float]:
    """
    Validate alphas
    Args:
        alphas (AlphaLike)

    Returns:
        List[float]
    """
    if isinstance(alphas, float):
        alphas = [alphas]

    _len_alphas = len(alphas)
    if _len_alphas == 0:
        raise ValidationException("Input alpha is not valid")

    if _len_alphas >= 2 and any(
        alphas[i] > alphas[i + 1] for i in range(_len_alphas - 1)
    ):
        raise ValidationException("Alpha is not ascending order")

    if _len_alphas != len(set(alphas)):
        raise ValidationException("Duplicated alpha exists")

    return alphas


def prepare_x(
    x: XdataLike,
    alphas: List[float],
) -> pd.DataFrame:
    """
    Return stacked X
    Args:
        x (XdataLike)
        alphas (List[float])

    Returns:
        pd.DataFrame
    """
    if isinstance(x, np.ndarray) or isinstance(x, pd.Series):
        x = pd.DataFrame(x)

    if "_tau" in x.columns:
        raise ValidationException("Column name '_tau' is not allowed.")

    _alpha_repeat_count_list = [list(repeat(alpha, len(x))) for alpha in alphas]
    _alpha_repeat_list = list(chain.from_iterable(_alpha_repeat_count_list))

    _repeated_x = pd.concat([x] * len(alphas), axis=0)
    _repeated_x = _repeated_x.assign(
        _tau=_alpha_repeat_list,
    )
    return _repeated_x


def prepare_y(
    y: YdataLike,
    alphas: List[float],
) -> np.ndarray:
    """
    Return stacked y
    Args:
        y (YdataLike)
        alphas (List[float])

    Returns:
        np.ndarray
    """
    return np.concatenate(list(repeat(y, len(alphas))))


def delta_validate(delta: float) -> float:
    _delta_upper_bound: float = 0.1

    if not isinstance(delta, float):
        raise ValidationException("delta is not float type")

    if delta > _delta_upper_bound:
        raise ValidationException("Delta must be smaller than 0.1")

    return delta
