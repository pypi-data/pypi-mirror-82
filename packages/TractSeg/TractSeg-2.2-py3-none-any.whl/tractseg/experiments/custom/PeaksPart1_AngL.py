import os
from tractseg.experiments.peak_reg import Config as PeakRegConfig

class Config(PeakRegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    CLASSES = "All_Part1"     # All_Part1 / All_Part2 / All_Part3 / All_Part4

    LOSS_WEIGHT = 1  # do not set to None otherwise does not pass weights to loss and angleLen expects weights
    LOSS_WEIGHT_LEN = -1
    LOSS_FUNCTION = "angle_loss"
    METRIC_TYPES = ["loss", "f1_macro"]
    BEST_EPOCH_SELECTION = "loss"
