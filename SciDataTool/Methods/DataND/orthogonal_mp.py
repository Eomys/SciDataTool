from SciDataTool.Classes.Data1D import Data1D
from SciDataTool.Functions.omp import omp, comp_undersampled_axe


def orthogonal_mp(
    self, Time: Data1D, n_coefs: int = None, precompute: bool = True, dictionary=None
):
    """
    Execute the Orthogonal Matching Pursuit, this method returns a DataND object with the Time axe,
    self is the DataND undersampled object.

    Parameters
    ----------
    Time: The time axe on which the signals are recovered
    M: The undersampling indices, Time.values[M] is the time axe of self
    n_coefs: The number of atoms of the dictionary used to recover the signal,
    if None set to 10 % of len(M)
    dictionary: A special dictionary which is pass to the backend

    Returns
    recovered_dataND: A new dataND object composed of the recovered components
    """

    # This method should only be used for 1D or 2D field, where the
    # undersampling is in the time's direction
    nombre_axes = len(self.axes)
    assert (
        nombre_axes == 2 or nombre_axes == 1
    ), "Dimension error: {} not in {1,2}".format(nombre_axes)

    axes_name = [self.axes[i].name for i in range(nombre_axes)]
    assert "time" in axes_name, "There is no time axe"
    axes_name.remove("time")

    # Extract the axes
    if nombre_axes == 2:
        [Angle] = self.get_axes(axes_name[0])
    [Time_undersampled] = self.get_axes("time")

    M = comp_undersampled_axe(Time, Time_undersampled)

    n = len(Time.values)

    # Stack the signals into the columns of the matrix Y (n,n_targets)
    Y = self.values

    # Compute the OMP
    Y_full = omp(Y, M, n, n_coefs=n_coefs, precompute=precompute, dictionary=dictionary)

    # Build the DataND object
    if nombre_axes == 1:
        recovered_dataND = type(self)(
            name=self.name,
            symbol=self.symbol,
            unit=self.unit,
            values=Y_full,
            axes=[Time],
            is_real=self.is_real,
        )
    if nombre_axes == 2:
        recovered_dataND = type(self)(
            name=self.name,
            symbol=self.symbol,
            unit=self.unit,
            axes=[Time, Angle],
            values=Y_full,
            is_real=self.is_real,
        )

    return recovered_dataND
