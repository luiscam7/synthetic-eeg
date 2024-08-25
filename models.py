"""
Define data models using Pydantic
"""

from typing import List

from pydantic import BaseModel


class EEGData(BaseModel):
    Fp1: List[float]
    Fp2: List[float]
    F3: List[float]
    F4: List[float]
    C3: List[float]
    Cz: List[float]
    C4: List[float]
    T3: List[float]
    O1: List[float]
    O2: List[float]
    P3: List[float]
    P4: List[float]
    F7: List[float]
    F8: List[float]
    T4: List[float]
    T5: List[float]
    T6: List[float]
    Fz: List[float]
    Pz: List[float]
