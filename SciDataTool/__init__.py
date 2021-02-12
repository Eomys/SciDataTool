# -*- coding: utf-8 -*-
from SciDataTool.Classes.Data import Data
from SciDataTool.Classes.Data1D import Data1D
from SciDataTool.Classes.DataFreq import DataFreq
from SciDataTool.Classes.DataTime import DataTime
from SciDataTool.Classes.DataLinspace import DataLinspace
from SciDataTool.Classes.DataND import DataND
from SciDataTool.Classes.RequestedAxis import RequestedAxis
from SciDataTool.Classes.VectorField import VectorField
from SciDataTool.Classes.DataPattern import DataPattern

__version__ = "1.1.5"

from os.path import normpath, join, abspath, dirname, isdir
from os import makedirs
from shutil import rmtree
from matplotlib import use

TEST_DIR = join(abspath(dirname(__file__)), "..", "Tests")
DATA_DIR = join(TEST_DIR, "Data")
LOG_DIR = join(TEST_DIR, "logtest.txt")
DOC_DIR = abspath(join(TEST_DIR, "..", "Doc"))
# Init the result folder for the test
save_path = join(TEST_DIR, "Results")
if isdir(save_path):  # Delete previous test result
    rmtree(save_path)
# To save all the plot geometry results
save_plot_path = join(save_path, "Plot")
makedirs(save_plot_path)
# To save the validation results
save_validation_path = join(save_path, "Validation")
makedirs(save_validation_path)
# To save the Save/Load .json results
save_load_path = join(save_path, "Save_Load")
makedirs(save_load_path)
# To save the GUI results
save_gui_path = join(save_path, "GUI")
makedirs(save_gui_path)
# To clean all the results at the end of the corresponding test
is_clean_result = False
