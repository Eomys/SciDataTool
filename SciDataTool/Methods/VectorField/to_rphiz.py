def to_rphiz(self):
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

    if (
        "radial" in self.components
        or "tangential" in self.components
        or "axial" in self.components
    ):
        return self.copy()

    else:
        # Coordinate transform
        arg_list = [
            axis.name
            if axis.name in ["freqs", "wavenumber"]
            else axis.name + "[smallestperiod]"
            for axis in self.components["comp_x"].axes
        ]
        result = self.get_rphiz_along(*arg_list)
        # Store in new VectorField
        comp_dict = dict()

        Comp_r = self.components["comp_x"].copy()
        Comp_r.name = "Radial " + self.components["comp_x"].name.lower().replace(
            " along x-axis", ""
        )
        Comp_r.symbol = self.components["comp_x"].symbol.replace("_x", "_r")
        Comp_r.values = result["radial"]
        comp_dict["radial"] = Comp_r

        Comp_t = self.components["comp_x"].copy()
        Comp_t.name = "Tangential " + self.components["comp_x"].name.lower().replace(
            " along x-axis", ""
        )
        Comp_t.symbol = self.components["comp_x"].symbol.replace("_r", "_y")
        Comp_t.values = result["tangential"]
        comp_dict["comp_y"] = Comp_t

        if "axial" in self.components:
            Comp_z = self.components["axial"].copy()
            comp_dict["comp_z"] = Comp_z

        return VectorField(name=self.name, symbol=self.symbol, components=comp_dict)
