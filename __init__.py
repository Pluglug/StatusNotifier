import bpy
import blf
# import os
from bpy.props import *
from bpy.types import Operator, AddonPreferences

import addon
from preferences import StatusNotifierAddonPreferences
from overlay import TEXT_OT_activate_handler, activate_handler, text_display_handler

bl_info = {
    "name": "Status Notifier",
    "author": "Pluglug",
    "version": (0, 6),
    "blender": (3, 6, 5),
    "location": "View3D",
    "description": "Monitor environment settings",
    "warning": "It'll explode.",
    "category": "User Interface"
}


addon.VERSION = bl_info["version"]
addon.BL_VERSION = bl_info["blender"]


def register():
    bpy.utils.register_class(StatusNotifierAddonPreferences)

    bpy.utils.register_class(TEXT_OT_activate_handler)
    bpy.app.timers.register(activate_handler, first_interval=1.0)

def unregister():
    text_display_handler.stop()
    bpy.utils.unregister_class(TEXT_OT_activate_handler)

    bpy.utils.unregister_class(StatusNotifierAddonPreferences)


if __name__ == "__main__":
    # push test
    pass
