"""Pydantic models for the web service."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class InputData(BaseModel):
    """Physical measurements of one abalone."""

    sex: Literal["M", "F", "I"]
    length: float = Field(gt=0)
    diameter: float = Field(gt=0)
    height: float = Field(gt=0)
    whole_weight: float = Field(gt=0)
    shucked_weight: float = Field(gt=0)
    viscera_weight: float = Field(gt=0)
    shell_weight: float = Field(gt=0)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sex": "M",
                "length": 0.455,
                "diameter": 0.365,
                "height": 0.095,
                "whole_weight": 0.514,
                "shucked_weight": 0.2245,
                "viscera_weight": 0.101,
                "shell_weight": 0.15,
            }
        }
    )


class PredictionOut(BaseModel):
    """Predicted number of rings and the matching age in years."""

    rings: float
    age: float
