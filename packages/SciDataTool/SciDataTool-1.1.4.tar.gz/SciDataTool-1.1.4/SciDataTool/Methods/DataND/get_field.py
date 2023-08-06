# -*- coding: utf-8 -*-
from numpy import sum as np_sum
from SciDataTool.Functions.symmetries import rebuild_symmetries


def get_field(self, axes_list):
    """Returns the values of the field (with symmetries and sums).
    Parameters
    ----------
    self: Data
        a Data object
    axes_list: list
        a list of RequestedAxis objects
    Returns
    -------
    values: ndarray
        values of the field
    """

    values = self.values
    for axis_requested in axes_list:
        # Rebuild symmetries only for fft case
        if (
            axis_requested.transform == "fft"
            and axis_requested.corr_name in self.symmetries.keys()
        ):
            if "antiperiod" in self.symmetries.get(axis_requested.corr_name):
                values = self.rebuild_symmetries(
                    values,
                    axis_requested.corr_name,
                    axis_requested.index,
                    is_oneperiod=True,
                    is_antiperiod=False,
                )

        # Sum over sum axes
        if axis_requested.extension == "sum":
            values = np_sum(values, axis=axis_requested.index)
    return values
