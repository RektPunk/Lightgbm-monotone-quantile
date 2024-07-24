from enum import StrEnum
from typing import Callable, Dict, List, Union

import lightgbm as lgb
import numpy as np
import pandas as pd
import xgboost as xgb


class BaseEnum(StrEnum):
    @classmethod
    def get(cls, text: str) -> "BaseEnum":
        cls._isin(text)
        return cls[text]

    @classmethod
    def _isin(cls, text: str) -> None:
        if text not in cls._member_names_:
            valid_members = ", ".join(cls._member_names_)
            raise ValueError(
                f"Invalid value: '{text}'. Expected one of: {valid_members}."
            )


# Name
class ModelName(BaseEnum):
    lightgbm: str = "lightgbm"
    xgboost: str = "xgboost"


class ObjectiveName(BaseEnum):
    check: str = "check"
    huber: str = "huber"


class TypeName(BaseEnum):
    train_dtype: str = "train_dtype"
    predict_dtype: str = "predict_dtype"
    constraints_type: str = "constraints_type"


class MQStr(BaseEnum):
    mono: str = "monotone_constraints"
    obj: str = "objective"
    valid: str = "valid"


# Functions
FUNC_TYPE: Dict[ModelName, Dict[TypeName, Callable]] = {
    ModelName.lightgbm: {
        TypeName.train_dtype: lgb.Dataset,
        TypeName.predict_dtype: lambda x: x,
        TypeName.constraints_type: list,
    },
    ModelName.xgboost: {
        TypeName.train_dtype: xgb.DMatrix,
        TypeName.predict_dtype: xgb.DMatrix,
        TypeName.constraints_type: tuple,
    },
}


# Type
XdataLike = Union[pd.DataFrame, pd.Series, np.ndarray]
YdataLike = Union[pd.Series, np.ndarray]
AlphaLike = Union[List[float], float]
ModelLike = Union[lgb.basic.Booster, xgb.Booster]
DtrainLike = Union[lgb.basic.Dataset, xgb.DMatrix]


# Exception
class FittingException(Exception):
    pass


class ValidationException(Exception):
    pass
