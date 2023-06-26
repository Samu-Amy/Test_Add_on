import bpy
from . import panel
from . import preferences
from . import operators
from . import _refresh_

_refresh_.reload_modules()

bl_info = {
    "name": "Structured Add-on",
    "description": "Add-on consisting of multiple files",
    "author": "Samu Amy",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Learning"
}


modules = [preferences, operators, panel]


def register():
    for mod in modules:
        mod.register_classes()


def unregister():
    for mod in modules:
        mod.unregister_classes()


if __name__ == "__main__":
    register()
