import bpy
from bpy.types import (
    Operator,
    AddonPreferences,
    PropertyGroup,
)
from bpy.props import (
    BoolProperty,
    EnumProperty,
    IntProperty,
    FloatVectorProperty,
)

from .dev.vlog import log
from .dev.flags import *


class StatusNotifierAddonPreferences(AddonPreferences):
    bl_idname = __name__

    overlay_offset_x: IntProperty(
        name="Overlay Offset X",
        description="Horizontal offset for the overlay",
        default=50)

    overlay_offset_y: IntProperty(
        name="Overlay Offset Y",
        description="Vertical offset for the overlay",
        default=50)

    overlay_alignment: EnumProperty(
        name="Overlay Alignment",
        description="Alignment of the overlay text",
        items=[
            ('TOP', "Top", ""),
            ('TOP_LEFT', "Top Left", ""),
            ('TOP_RIGHT', "Top Right", ""),
            ('BOTTOM', "Bottom", ""),
            ('BOTTOM_LEFT', "Bottom Left", ""),
            ('BOTTOM_RIGHT', "Bottom Right", "")],
        default='BOTTOM')

    text_size: IntProperty(
        name="Text Size",
        description="Size of the text",
        default=50)

    text_color: FloatVectorProperty(
        name="Text Color",
        description="Color of the text",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.5, 0.0, 1.0))

    line_offset: IntProperty(
        name="Line Offset",
        description="Offset for the next line",
        default=10)

    show_text: BoolProperty(
        name="Show Text",
        description="Whether to show text or not",
        default=True)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "show_text", text="Show Text", toggle=True)

        box = layout.box()
        box.prop(self, "overlay_alignment", text="Overlay Alignment")

        alignment = self.overlay_alignment
        is_alignment_top_or_bottom = alignment in {"TOP", "BOTTOM"}

        row = box.row(align=True)
        row.prop(self, "overlay_offset_x", text="Offset X") if not is_alignment_top_or_bottom else None
        row.prop(self, "overlay_offset_y", text="Offset Y")

        row = box.row(align=True)
        row.prop(self, "text_size", text="Text Size")
        row.prop(self, "line_offset", text="Line Offset")

        box.prop(self, "text_color", text="Text Color")

        messages = [
            "Notes:",
            "No UI is provided to increase the number of properties you want to monitor.",
            "Currently you need to adjust the `generate_text_lines` function.",
            "Ask ChatGPT to add any additional conditions you would like to add to this section."
        ]

        for msg in messages:
            layout.label(text=msg, icon='ERROR' if msg == messages[0] else 'NONE')
