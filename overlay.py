import bpy
import blf

from addon import is_40

from debug import log, DBG_INIT, DBG_OPS, DBG_HANDLERS, log_exec


def blf_size(font_id, size):
    if is_40():
        blf.size(font_id, size)
    else:
        blf.size(font_id, size, 72)


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


class TEXT_OT_activate_handler(bpy.types.Operator):
    """Activate the text display handler"""
    bl_idname = "text.activate_handler"
    bl_label = "Activate Text Handler"

    @classmethod
    def poll(cls, context):
        return not text_display_handler.is_active()

    @log_exec
    def execute(self, context):
        text_display_handler.start(context)
        return {'FINISHED'}


class TEXT_OT_deactivate_handler(bpy.types.Operator):
    """Deactivate the text display handler"""
    bl_idname = "text.deactivate_handler"
    bl_label = "Deactivate Text Handler"

    @classmethod
    def poll(cls, context):
        return text_display_handler.is_active()

    @log_exec
    def execute(self, context):
        text_display_handler.stop()
        return {'FINISHED'}


def activate_handler():
    bpy.ops.text.activate_handler()
    return None  # Stop the timer


if __name__ == "__main__":
    pass
