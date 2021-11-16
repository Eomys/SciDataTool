def to_xyz(self):
    """Performs the corrdinate change and stores the resulting field in a VectorField object.
    Parameters
    ----------
    self : VectorField
        a VectorField object
    Returns
    -------
    a VectorField object
    """

    # Dynamic import to avoid loop
    module = __import__("SciDataTool.Classes.VectorField", fromlist=["VectorField"])
    VectorField = getattr(module, "VectorField")

    if "comp_x" in self.components or "comp_y" in self.components:
        return self.copy()

    else:
        # Coordinate transform
        arg_list = [
            axis.name
            if axis.name in ["freqs", "wavenumber"]
            else axis.name + "[smallestperiod]"
            for axis in self.components["radial"].axes
        ]
        result = self.get_xyz_along(*arg_list, is_squeeze=False)
        # Store in new VectorField
        comp_dict = dict()

        Comp_x = self.components["radial"].copy()
        Comp_x.name = (
            self.components["radial"].name.lower().replace("radial ", "")
            + " along x-axis"
        )
        Comp_x.symbol = self.components["radial"].symbol.replace("_r", "_x")
        Comp_x.values = result["comp_x"]
        comp_dict["comp_x"] = Comp_x

        Comp_y = self.components["radial"].copy()
        Comp_y.name = (
            self.components["radial"].name.lower().replace("radial ", "")
            + " along y-axis"
        )
        Comp_y.symbol = self.components["radial"].symbol.replace("_r", "_y")
        Comp_y.values = result["comp_y"]
        comp_dict["comp_y"] = Comp_y

        if "axial" in self.components:
            Comp_z = self.components["axial"].copy()
            comp_dict["comp_z"] = Comp_z

        return VectorField(name=self.name, symbol=self.symbol, components=comp_dict)
