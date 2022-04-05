import matplotlib.pyplot as plt
from numpy import arange, nanmax, nanmin, frombuffer
import imageio
from ...GUI.DDataPlotter.DDataPlotter import PARAM_2D


def plot_3D_Data_Animated(
    self, animated_axis, suptitle_ref, *param_list, nb_frames=50, fps=10, **param_dict
):
    """Gen

    Parameters
    ----------
    animated_axis : str
        The field will be animated along this axis
    nb_frames : int
        number of frames used to build the gif
    fps: int
        frames displayed per second
    """

    # Relative import of DataPattern to prevent circular import
    module = __import__("SciDataTool.Classes.DataPattern", fromlist=["DataPattern"])
    DataPattern = getattr(module, "DataPattern")

    # Making sure that we have the right argument for a plot3D
    plot_options = param_dict.copy()
    for param in PARAM_2D:
        if param in plot_options:
            del plot_options[param]

    # Detecting if animated axis is a DataPattern, if true changing the input given to the function
    for ax_obj in self.get_axes():
        if ax_obj.name == animated_axis.split("[")[0]:
            animated_axis_obj = ax_obj
            break

    if isinstance(animated_axis_obj, DataPattern):
        # Removing one_period as it is not available with a DataPattern
        animated_axis_unit = "{" + animated_axis.split("{")[1]
        animated_axis = animated_axis.split("[")[0] + animated_axis_unit

    if "freqs" in param_list or "wavenumber" in param_list:
        result = self.get_magnitude_along(animated_axis, *param_list)
    else:
        result = self.get_along(animated_axis, *param_list)

    animated_axis_unit = "{" + animated_axis.split("{")[1]
    animated_axis = animated_axis.split("{")[0].split("[")[0]

    # Creating a list of frames that will need to create the animation
    if isinstance(animated_axis_obj, DataPattern):
        frames_list = animated_axis_obj.get_values()
        frames_list = [
            "[" + str(idx_frame) + "]" for idx_frame in range(len(frames_list))
        ]
        fps = 1
    else:
        value_max = nanmax(result[animated_axis])
        value_min = nanmin(result[animated_axis])
        variation_step = (value_max - value_min) / nb_frames

        frames_list = arange(start=value_min, stop=value_max, step=variation_step)
        frames_list = ["=" + str(frame) for frame in frames_list]

    plot_options["is_show_fig"] = False

    # Getting the name of the gif
    save_path = plot_options["save_path"].replace(".png", ".gif")
    plot_options["save_path"] = None

    images = list()  # List of images used to build the gif
    for val in frames_list:
        # plotting image
        self.plot_3D_Data(
            *param_list, animated_axis + val + animated_axis_unit, **plot_options
        )
        # Getting the figure generated with plot_2D_DATA
        fig = plt.gcf()

        # Adding the suptitle of the figure if there is one
        if suptitle_ref != "":
            fig.suptitle(suptitle_ref)

        fig.canvas.draw()
        image = frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)

        # Creating the gif
        plt.close(fig)

    imageio.mimsave(save_path, images, format="GIF-PIL", fps=fps)
