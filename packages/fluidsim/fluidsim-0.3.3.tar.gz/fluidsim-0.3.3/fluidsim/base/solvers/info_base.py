"""Base solver (:mod:`fluidsim.base.solvers.info_base`)
=======================================================

.. autoclass:: InfoSolverBase
   :members:
   :private-members:

"""

from copy import deepcopy

from fluiddyn.util.paramcontainer import ParamContainer
from fluiddyn.util import import_class


def create_info_simul(info_solver, params):
    """Create a ParamContainer instance gathering info_solver and params."""
    info = ParamContainer(tag="info_simul")
    info._set_as_child(info_solver)
    info._set_as_child(params)
    return info


def _merged_element(el1, el2):
    result = deepcopy(el1)
    result.extend(deepcopy(el2))
    return result


class InfoSolverBase(ParamContainer):
    """Contain the information on a solver."""

    def __init__(self, **kargs):

        if len(kargs) == 0 or ("path_file" in kargs and "tag" not in kargs):
            kargs["tag"] = "solver"

        super().__init__(**kargs)

        if (
            "tag" in kargs
            and kargs["tag"] == "solver"
            and "path_file" not in kargs
        ):
            self._init_root()

    def _init_root(self):

        self._set_attribs(
            {
                "module_name": "fluidsim.base.solvers.base",
                "class_name": "SimulBase",
                "short_name": "Base",
            }
        )

        classes = self._set_child("classes")

        classes._set_child(
            "Operators",
            attribs={
                "module_name": "fluidsim.operators.operators0d",
                "class_name": "Operators0D",
            },
        )

        classes._set_child(
            "State",
            attribs={
                "module_name": "fluidsim.base.state",
                "class_name": "StateBase",
            },
        )

        classes._set_child(
            "TimeStepping",
            attribs={
                "module_name": "fluidsim.base.time_stepping.simple",
                "class_name": "TimeSteppingSimple",
            },
        )

        classes._set_child(
            "InitFields",
            attribs={
                "module_name": "fluidsim.base.init_fields",
                "class_name": "InitFieldsBase",
            },
        )

        classes._set_child(
            "Forcing",
            attribs={
                "module_name": "fluidsim.base.forcing",
                "class_name": "ForcingBase",
            },
        )

        classes._set_child(
            "Output",
            attribs={
                "module_name": "fluidsim.base.output.base",
                "class_name": "OutputBase",
            },
        )

    def import_classes(self):
        """Import the classes and return a dictionary."""
        if hasattr(self, "_cached_imported_classes"):
            return self._cached_imported_classes

        dict_classes = {}
        tags = self.classes._tag_children
        if len(tags) == 0:
            self._set_internal_attr("_cached_imported_classes", dict_classes)
            return dict_classes

        for tag in tags:
            cls = self.classes.__dict__[tag]
            try:
                module_name = cls.module_name
                class_name = cls.class_name
            except AttributeError:
                pass
            else:
                Class = import_class(module_name, class_name)
                dict_classes[cls._tag] = Class

        self._set_internal_attr("_cached_imported_classes", dict_classes)
        return dict_classes

    def complete_with_classes(self):
        dict_classes = self.import_classes()
        for Class in list(dict_classes.values()):
            if hasattr(Class, "_complete_info_solver"):
                Class._complete_info_solver(self)
