"""Common utilities"""

from inspect import isgenerator
import io

import pandas as pd
from pyexcel.internal import SOURCE
from pyexcel_xlsx import get_data as get_xlsx, save_data as save_xlsx
from pyexcel_xls import get_data as get_xls, save_data as save_xls
from toolbox import st, is_str, MappingMixin

XLS = "xls"
XLSX = "xlsx"


def is_pandas(o):
    return isinstance(o, (pd.DataFrame, pd.Series, pd.Panel))


def is_file_obj(o):
    return isinstance(o, (io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase))


def iterize(o):
    """Automatically wrap certain objects that you would not normally process item by item"""
    if (
        is_pandas(o)
        or is_str(o)
        or is_file_obj(o)
        or isinstance(o, dict)
        or callable(o)
    ):
        return [o]
    return o


def excel_file_type(f):
    """Best guess at Excel file type from name"""
    if isinstance(f, str):
        if f.endswith(XLS):
            return XLS
        if f.endswith(XLSX):
            return XLSX
        assert False, "Unsupported Excel file: %s" % f
    else:
        if hasattr(f, "name") and f.name.endswith(XLS):
            return XLS
        # Just assumes it's an .xlsx file
        return XLSX


def read_excel(f, **kwargs):
    """Read data from an Excel file using pyexcel

    Parameters
    ----------
    f : str or buffer
        Excel file to read from
    **kwargs
        Keyword arguments passed to pyexcel

    """
    excel_type = excel_file_type(f)
    if excel_type == XLS:
        data = get_xls(f, **kwargs)
    else:
        data = get_xlsx(f, **kwargs)
    return data


def save_excel(f, data, **kwargs):
    """Write data to an Excel file using pyexcel

    Note
    ----
    If f is a file that ends in .xls, pyexcel_xls will be used, otherwise it
    defaults to pyexcel_xlsx.

    Parameters
    ----------
    f : str or buffer
        Excel file to write to
    data : dict
        Data to write to the file. This is expected to be a dict of
        {sheet_name: sheet_data} format.
    **kwargs
        Keyword arguments passed to pyexcel's save_data

    """
    excel_type = excel_file_type(f)
    if excel_type == XLS:
        save_xls(f, data, **kwargs)
    else:
        save_xlsx(f, data, **kwargs)
