import bpy
import os


VERSION = None
BL_VERSION = None
ADDON_ID = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
ADDON_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
ICON_ENUM_ITEMS = bpy.types.UILayout.bl_rna.functions[
    "prop"].parameters["icon"].enum_items


def uprefs():
    return getattr(bpy.context, "user_preferences", None) or \
        getattr(bpy.context, "preferences", None)


def prefs():
    return uprefs().addons[ADDON_ID].preferences


def is_40():
    return bpy.app.version >= (4, 0, 0)
