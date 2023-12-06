import bpy
from debug import log, DBG_TEXT

from test_data import *


alignment_items = [
    ('TOP', "Top", ""),
    ('TOP_LEFT', "Top Left", ""),
    ('TOP_RIGHT', "Top Right", ""),
    ('BOTTOM', "Bottom", ""),
    ('BOTTOM_LEFT', "Bottom Left", ""),
    ('BOTTOM_RIGHT', "Bottom Right", ""),
]


class DisplayText(bpy.types.PropertyGroup):
    is_active: bpy.props.BoolProperty(name="Is Active", default=False)
    text: bpy.props.StringProperty(name="Text", default="Text")
    condition: bpy.props.StringProperty(name="Condition", default="True")

    size: bpy.props.IntProperty(name="Size", default=50)
    color: bpy.props.FloatVectorProperty(
        name="Color",
        description="Color of the text",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.5, 0.0, 1.0))

    align: bpy.props.EnumProperty(
        name="Alignment",
        description="Alignment of the overlay text",
        items=alignment_items,
        default='BOTTOM')
    offset_x: bpy.props.IntProperty(name="Offset X", default=50)
    offset_y: bpy.props.IntProperty(name="Offset Y", default=50)


class GenTextLines:

    def __init__(self):
        pass

    def eval(self, expression):
        value = None
        try:
            value = eval(expression, globals(), locals())
        except:
            log.error("Error evaluating expression: {}".format(expression))
        return value

    def get_text_lines(self):
        text_lines = []
        for text, condition in console_test_data:
            if self.eval(condition):
                text_lines.append(text)
        text_lines = list(reversed(text_lines))
        return text_lines


if __name__ == "__main__":
    # log.header("GenTextLines Test")
    # gtl = GenTextLines()
    # for text, condition in console_test_data:
    #     log.info("{}: {}".format(text, gtl.eval(condition)))
    # log.header("get_text_lines()")
    # log.info(gtl.get_text_lines())
    pass
