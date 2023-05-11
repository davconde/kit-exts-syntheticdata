import omni.ext
from .scripts.window import SDGWindow


# Functions and vars are available to other extension as usual in python:
# `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[davconde.syntheticdata.generator] "
          "some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module
# (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)`
# will be called. Later when extension gets disabled
# on_shutdown() is called.
class DavcondeSyntheticdataGeneratorExtension(omni.ext.IExt):
    # ext_id is current extension id.
    # It can be used with extension manager to query additional information,
    # like where this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[davconde.syntheticdata.generator] "
              "davconde syntheticdata generator startup")
        self._window = SDGWindow(
            "Synthetic Data Generator",
            width=600, height=400)

    def on_shutdown(self):
        print("[davconde.syntheticdata.generator] "
              "davconde syntheticdata generator shutdown")
        self._window.destroy()
        self._window = None
