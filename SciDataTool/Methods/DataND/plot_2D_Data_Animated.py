import matplotlib.pyplot as plt
import numpy as np
import imageio
from SciDataTool.Methods.DataND.plot_2D_Data import plot_2D_Data


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
    value_max = np.max(self.get_axes(animated_axis)[0].get_values())
    value_min = np.min(self.get_axes(animated_axis)[0].get_values())
    value_variation_step = (value_max - value_min) / nb_frames

    param_dict['y_min'] = np.min(self.values)
    param_dict['y_max'] = np.max(self.values)
    param_dict['is_show_fig'] = False
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
        value_min += value_variation_step
    # Creating the gif
    imageio.mimsave(save_path, images, format="GIF-PIL", fps=fps)
