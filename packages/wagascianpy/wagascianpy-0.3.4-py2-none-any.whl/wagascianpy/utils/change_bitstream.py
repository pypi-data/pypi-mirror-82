#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio, Eguchi Aoi
import os
import shutil
from six import string_types
from wagascianpy.utils.environment import WagasciEnvironment
import wagascianpy.utils.utils
import wagascianpy.analysis.analysis

_CHANGE_INPUTDAC_MODE = 2
_CHANGE_THRESHOLD_MODE = 0
_CHANGE_CHIPID_MODE = 5


###############################################################################
#                                change_bitstream                                #
###############################################################################

def change_bitstream(dif_topology, bitstream_root_dir, input_dac, trigger_threshold):
    """
    Change the global input DAC and global trigger threshold bitstream
    parameters for all the chips.

    Args:
        dif_topology: DIF topology dictionary
        bitstream_root_dir: root directory for the bistream folder tree
        input_dac: global input DAC value (0-255)
        trigger_threshold: global trigger threshold (0-1023)

    Returns:
        None

    Exceptions:
        ValueError if the arguments are empty or invalid
    """
    # Check sanity of arguments

    if not isinstance(dif_topology, dict):
        raise ValueError("[change_bitstream] DIF topology is not a dictionary")
    if not dif_topology:
        raise ValueError("[change_bitstream] DIF topology is empty")
    if not isinstance(bitstream_root_dir, string_types):
        raise ValueError("[change_bitstream] bitstream_dir is not a directory")
    if not bitstream_root_dir:
        raise ValueError("[change_bitstream] bitstream_dir is empty")
    bitstream_root_dir = bitstream_root_dir.rstrip("/")
    wagascianpy.utils.utils.mkdir_p(bitstream_root_dir)
    input_dac = int(input_dac)
    if input_dac < 0 or input_dac > 255:
        raise ValueError("[change_bitstream] input DAC value is not valid : %d"
                         % input_dac)
    trigger_threshold = int(trigger_threshold)
    if trigger_threshold < 0 or trigger_threshold > 1023:
        raise ValueError("[change_bitstream] trigger threshold value is not valid : %d"
                         % trigger_threshold)

    environ = WagasciEnvironment()
    try:
        bitstream_template = environ['WAGASCI_CONFDIR'] + "/wagasci_bitstream_template.txt"
    except KeyError as error:
        raise KeyError("Could not find WAGASCI configuration directory : {}".format(str(error)))
    try:
        process = wagascianpy.analysis.analysis.WagasciAnalysis(environ['WAGASCI_LIBDIR'])
    except KeyError as error:
        raise KeyError("Could not find WAGASCI library directory : {}".format(str(error)))
    overwrite_flag = True
    edit_flag = True

    for dif, chip_map in sorted(iter(dif_topology.items()),
                                key=lambda item: int(item[0])):
        for chip, n_channels in sorted(iter(chip_map.items()),
                                       key=lambda item: int(item[0])):
            chip_bitstream = "%s/wagasci_bitstream_dif%s_chip%02d.txt" \
                             % (bitstream_root_dir, dif, int(chip))
            if not os.path.isfile(chip_bitstream):
                shutil.copyfile(bitstream_template, chip_bitstream)
            # Input DAC
            for channel in range(wagascianpy.analysis.analysis.SPIROC2D_NCHANNELS):
                input_dac_value = input_dac
                if channel >= int(n_channels):
                    input_dac_value = -1
                result = process.change_config(chip_bitstream,
                                               chip_bitstream,
                                               overwrite_flag,
                                               edit_flag,
                                               input_dac_value,
                                               _CHANGE_INPUTDAC_MODE,
                                               channel)
                if result != 0:
                    raise ValueError("[change_bitstream] Error while changing "
                                     "input DAC : %d" % result)
            # Threshold
            result = process.change_config(chip_bitstream,
                                           chip_bitstream,
                                           overwrite_flag,
                                           edit_flag,
                                           trigger_threshold,
                                           _CHANGE_THRESHOLD_MODE)
            if result != 0:
                raise ValueError("[change_bitstream] Error while changing "
                                 "global threshold : %d" % result)
            # Chip ID
            result = process.change_config(chip_bitstream,
                                           chip_bitstream,
                                           overwrite_flag,
                                           edit_flag,
                                           chip,
                                           _CHANGE_CHIPID_MODE)
            if result != 0:
                raise ValueError("[change_bitstream] Error while changing "
                                 "Chip ID : %d" % result)
