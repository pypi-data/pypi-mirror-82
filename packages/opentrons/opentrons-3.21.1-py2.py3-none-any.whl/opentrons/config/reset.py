import logging
import os
import shutil
from enum import Enum
from pathlib import Path
from typing import NamedTuple, Dict, Set

from opentrons.config import (robot_configs as rc,
                              IS_ROBOT, feature_flags as ff)
from opentrons.data_storage import database as db
from opentrons.calibration_storage import delete

DATA_BOOT_D = Path('/data/boot.d')

log = logging.getLogger(__name__)


class UnrecognizedOption(Exception):
    pass


class CommonResetOption(NamedTuple):
    name: str
    description: str


class ResetOptionId(str, Enum):
    """The available reset options"""
    tip_probe = 'tipProbe'
    labware_calibration = 'labwareCalibration'
    boot_scripts = 'bootScripts'


_common_settings_reset_options = {
    ResetOptionId.tip_probe:
        CommonResetOption(
            name='Pipette Calibration',
            description='Clear pipette offset and tip length calibration'
        ),
    ResetOptionId.labware_calibration:
        CommonResetOption(
            name='Labware Calibration',
            description='Clear labware calibration and Protocol API v1 custom labware (created with labware.create())'   # noqa(E501)
        ),
    ResetOptionId.boot_scripts:
        CommonResetOption(
            name='Boot Scripts',
            description='Clear custom boot scripts'
        ),
}


def reset_options() -> Dict[ResetOptionId, CommonResetOption]:
    return _common_settings_reset_options


def reset(options: Set[ResetOptionId]) -> None:
    """
    Execute a reset of the requested parts of the user configuration.

    :param options: the parts to reset
    """
    log.info("Reset requested for %s", options)
    if ResetOptionId.tip_probe in options:
        reset_tip_probe()

    if ResetOptionId.labware_calibration in options:
        reset_labware_calibration()

    if ResetOptionId.boot_scripts in options:
        reset_boot_scripts()


def reset_boot_scripts():
    if IS_ROBOT:
        if os.path.exists(DATA_BOOT_D):
            shutil.rmtree(DATA_BOOT_D)
    else:
        log.debug(f'Not on pi, not removing {DATA_BOOT_D}')


def reset_labware_calibration():
    delete.clear_calibrations()
    db.reset()


def reset_tip_probe():
    config = rc.load()
    config = config._replace(
        instrument_offset=rc.build_fallback_instrument_offset({}))
    if ff.enable_calibration_overhaul():
        delete.clear_tip_length_calibration()
    else:
        config.tip_length.clear()
    rc.save_robot_settings(config)
