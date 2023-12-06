import bpy

from addon import VERSION, BL_VERSION
from preferences import StatusNotifierAddonPreferences
from overlay import TEXT_OT_activate_handler, activate_handler

from debug import log, DBG_INIT


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


VERSION = bl_info["version"]
BL_VERSION = bl_info["blender"]


classes = [
    StatusNotifierAddonPreferences,
    TEXT_OT_activate_handler,
    TEXT_OT_deactivate_handler
]


def register():
    DBG_INIT and log.header("Registering addon...")
    for cls in classes:
        bpy.utils.register_class(cls)
        DBG_INIT and log.info("Registered class: %s", cls)
    bpy.app.timers.register(activate_handler, first_interval=1.0)


def unregister():
    # text_display_handler.stop()
    bpy.ops.text.deactivate_handler()
    DBG_INIT and log.header("Unregistering addon...")
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        DBG_INIT and log.info("Unregistered class: %s", cls)


if __name__ == "__main__":
    pass
