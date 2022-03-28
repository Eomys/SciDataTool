from matplotlib import use

# Set Matplotlib backend
use("Qt5Agg")  # Use PySide2 backend


def update_cb_enable(combobox):
    # To disable a combobox with only one item
    if combobox.count() <= 1:
        combobox.setEnabled(False)
    else:
        combobox.setEnabled(True)


from os.path import dirname, abspath, join

DATA_DIR = join(abspath(dirname(__file__)), "Results")
