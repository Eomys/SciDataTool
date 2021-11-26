import matplotlib.pyplot as plt
import numpy as np
import imageio


def plot_2D_Data_Animated(
    self, animated_axis, *param_list, nb_frames=50, fps=10, **param_dict
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

    # The list of images used to build the gif
    images = list()
    if "freqs" in param_list or "wavenumber" in param_list:
        result = self.get_magnitude_along(animated_axis, *param_list)
    else:
        result = self.get_along(animated_axis, *param_list)

    value_max = np.nanmax(result[animated_axis])
    value_min = np.nanmin(result[animated_axis])
    variation_step = (value_max - value_min) / nb_frames

    y_max = np.nanmax(result[self.symbol])
    y_min = np.nanmin(result[self.symbol])
    marge = (
        y_max - y_min
    ) * 0.05  # 5% of the height of plot to add to the border top/bottom of gif
    param_dict["y_min"] = np.nanmin(result[self.symbol]) - abs(marge)
    param_dict["y_max"] = np.nanmax(result[self.symbol]) + abs(marge)
    param_dict["is_show_fig"] = False
    # Getting the name of the gif
    save_path = param_dict["save_path"].replace(".png", ".gif")
    param_dict["save_path"] = None
    while value_min < value_max:
        # plotting image
        self.plot_2D_Data(
            *param_list, animated_axis + "=" + str(value_min), **param_dict
        )
        # Getting the figure generated with plot_2D_DATA
        fig = plt.gcf()
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)
        plt.close(fig)
        value_min += variation_step
    # Creating the gif
    imageio.mimsave(save_path, images, format="GIF-PIL", fps=fps)
