"""

Submodules
==========

.. autosummary::
    :toctree: _autosummary


"""

__all__ = (
    "CarInputParameters",
    "fill_xarray_from_input_parameters",
    "modify_xarray_from_custom_parameters",
    "get_standard_driving_cycle",
    "CarModel",
    "NoiseEmissionsModel",
    "HotEmissionsModel",
    "InventoryCalculation",
    "BackgroundSystemModel",
    "ExportInventory",
    "InternalNoiseModel"
)
__version__ = (1, 2, 6)

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


from .car_input_parameters import CarInputParameters
from .array import (
    fill_xarray_from_input_parameters,
    modify_xarray_from_custom_parameters,
)
from .noise_emissions import NoiseEmissionsModel
from .internal_noise import InternalNoiseModel
from .hot_emissions import HotEmissionsModel
from .driving_cycles import get_standard_driving_cycle
from .model import CarModel
from .inventory import InventoryCalculation
from .background_systems import BackgroundSystemModel
from .export import ExportInventory
