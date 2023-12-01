import bpy
import blf
# import os
from bpy.props import *
from bpy.types import Operator, AddonPreferences

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


# Although is_40 is defined in this module for ease of distribution, 
# it should actually be defined in the `addon` module.
def is_40():
    return bpy.app.version >= (4, 0, 0)

def blf_size(font_id, size):
    if is_40():
        blf.size(font_id, size)
    else:
        blf.size(font_id, size, 72)


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


def get_screen_position(context, text, alignment, offset_x, offset_y, font_id=0):
    # Determine the x, y position based on alignment
    region = context.region
    width, height = region.width, region.height

    text_width, text_height = blf.dimensions(font_id, text)
    
    if 'TOP' in alignment:
        y = height - text_height - offset_y
    elif 'BOTTOM' in alignment:
        y = offset_y
    else:
        # Center vertically if neither TOP nor BOTTOM
        y = (height - text_height) / 2

    if 'LEFT' in alignment:
        x = offset_x
    elif 'RIGHT' in alignment:
        x = width - text_width - offset_x
    else:
        # Center horizontally if neither LEFT nor RIGHT
        x = (width - text_width) / 2  # + offset_x

    return (x, y)

# TODO: Currently, this function must be rewritten directly, 
# However, in the future, users will be able to add and remove conditions at will on the UI. 
# And it will be possible to set the position and text color for each condition.
# It should be implemented in about 10 years. Or someone else will.
def generate_text_lines(context):
    text_lines = []
    mode = context.mode
    tool_settings = context.tool_settings
    
    # Custom flag and text
    # usage: https://blenderartists.org/t/pie-menu-editor-1-18-7/662456/4885?u=pluglug
    if hasattr(context.scene, 'my_custom_flag') and context.scene.my_custom_flag:
        custom_text = context.scene.my_custom_text if hasattr(context.scene, 'my_custom_text') else ""
        text_lines.append(custom_text)

    # Edit Mesh specific condition
    if mode == 'EDIT_MESH':
        # Check if the Boxcutter tool is active
        if context.workspace.tools.from_space_view3d_mode('EDIT_MESH').idname == "Boxcutter":
            text_lines.append("Boxcutter")

        # Check if use_transform_correct_face_attributes is True
        if getattr(tool_settings, "use_transform_correct_face_attributes", False):
            if getattr(tool_settings, "use_transform_correct_keep_connected", False):
                text_lines.append("Correct Face Attributes (Keep Connected)")
            else:
                text_lines.append("Correct Face Attributes")

        if getattr(tool_settings, "use_edge_path_live_unwrap", False):
            text_lines.append("Live Unwrap")

    # Object Mode specific conditions
    if mode == 'OBJECT':
        # Check if the Boxcutter tool is active
        if context.workspace.tools.from_space_view3d_mode('OBJECT').idname == "Boxcutter":
            text_lines.append("Boxcutter")
        
        # Check if use_transform_data_origin is True
        if getattr(tool_settings, "use_transform_data_origin", False):
            text_lines.append("Affect Only Origin")

        # Check if Transform Pivot Point Align is enabled
        if getattr(tool_settings, "use_transform_pivot_point_align", False):
            text_lines.append("Affect Only Locations")

        # Check if Transform Skip Children is enabled
        if getattr(tool_settings, "use_transform_skip_children", False):
            text_lines.append("Affect Only Parents")

    # Pose Mode specific conditions
    if mode == 'POSE':
        pose = context.active_object.pose
        # Check if auto IK is enabled
        if pose and pose.use_auto_ik:
            text_lines.append("Auto IK")
        # Check if X-Mirror is enabled
        if pose and pose.use_mirror_x:
            # Check if Relative Mirror is enabled
            if pose and pose.use_mirror_relative:
                text_lines.append("X-Mirror (Relative)")
            else:
                text_lines.append("X-Mirror")

        # Check if Transform Pivot Point Align is enabled
        if tool_settings.use_transform_pivot_point_align:
            text_lines.append("Affect Only Locations")

    text_lines = list(reversed(text_lines))
    
    return text_lines


class TextDisplayHandler:
    def __init__(self):
        self.draw_handler = None

    def start(self, context):
        if self.draw_handler is None:
            self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')

    def stop(self):
        if self.draw_handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
            self.draw_handler = None

    def is_active(self):
        return self.draw_handler is not None
    
    def draw_callback(self, context):
        prefs = context.preferences.addons[__name__].preferences

        # Generate the text lines based on the current context
        text_lines = generate_text_lines(context)

        # Check if text should be displayed
        if not prefs.show_text or not text_lines:
            return

        font_id = 0
        blf_size(font_id, prefs.text_size)  # Set font size from addon preferences
        blf.color(font_id, *prefs.text_color)  # Set text color from addon preferences

        # Get the initial value of y_offset
        y_offset = prefs.overlay_offset_y
        
        for text in text_lines:
            # Get the screen position for the text based on the alignment
            x, y = get_screen_position(context, text, prefs.overlay_alignment, prefs.overlay_offset_x, y_offset, font_id)

            # Draw the text at the calculated position
            blf.position(font_id, x, y, 0)
            blf.draw(font_id, text)

            # Calculate the height of the text
            text_height = blf.dimensions(font_id, text)[1]

            # Adjust y_offset for the next line depending
            y_offset += (text_height + prefs.line_offset)


text_display_handler = TextDisplayHandler()


class TEXT_OT_activate_handler(Operator):
    """Activate the text display handler"""
    bl_idname = "text.activate_handler"
    bl_label = "Activate Text Handler"

    def execute(self, context):
        text_display_handler.start(context)
        return {'FINISHED'}

def activate_handler():
    bpy.ops.text.activate_handler()
    return None


def register():
    bpy.utils.register_class(StatusNotifierAddonPreferences)

    bpy.utils.register_class(TEXT_OT_activate_handler)
    bpy.app.timers.register(activate_handler, first_interval=1.0)

def unregister():
    text_display_handler.stop()
    bpy.utils.unregister_class(TEXT_OT_activate_handler)
    # bpy.app.timers.unregister(activate_handler)

    bpy.utils.unregister_class(StatusNotifierAddonPreferences)


if __name__ == "__main__":
    pass