import os

from tools import build


build.build(
    withconsole=False,
    path=os.path.abspath("Minkoww.py"),
    file_dict=None,
    companyname="shiüo",
    product_version="0.0.1",
    icon=None,
    plugin_dict=["pyside6"],
    include_package_dict=None
)