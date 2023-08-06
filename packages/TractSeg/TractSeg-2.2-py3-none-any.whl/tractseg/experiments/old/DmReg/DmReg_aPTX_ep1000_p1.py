#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.libs import exp_utils
from tractseg.experiments.base_legacy.dm_reg_legacy import Config as DmRegConfig


class Config(DmRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    P_SAMP = 1.

    CLASSES = "AutoPTX"
    NR_OF_CLASSES = len(exp_utils.get_bundle_names(CLASSES)[1:])

    THRESHOLD = 0.001
    NUM_EPOCHS = 1000
