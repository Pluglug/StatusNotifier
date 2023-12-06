import bpy
from debug import log

display_text_and_conditions = [
    ("Boxcutter", "C.active_object.mode == 'OBJECT' and context.workspace.tools.from_space_view3d_mode('OBJECT').idname == 'Boxcutter'"),
    ("Affect Only Origin", "C.active_object.mode == 'OBJECT' and getattr(C.active_object, 'use_transform_data_origin', False)"),
    ("Affect Only Locations", "C.active_object.mode == 'OBJECT' and getattr(C.active_object, 'use_transform_pivot_point_align', False)"),
    ("Affect Only Parents", "C.active_object.mode == 'OBJECT' and getattr(C.active_object, 'use_transform_skip_children', False)"),
    ("Auto IK", "C.active_object.mode == 'POSE' and C.active_object.pose and C.active_object.pose.use_auto_ik"),
    ("X-Mirror (Relative)", "C.active_object.mode == 'POSE' and C.active_object.pose and C.active_object.pose.use_mirror_x and C.active_object.pose.use_mirror_relative"),
    ("X-Mirror", "C.active_object.mode == 'POSE' and C.active_object.pose and C.active_object.pose.use_mirror_x"),
    ("Affect Only Locations", "C.active_object.mode == 'POSE' and getattr(C.active_object, 'use_transform_pivot_point_align', False)"),
]


console_test_data = [
    ("Boxcutter", "True and True"),
    ("Affect Only Origin", "True and False"),
    ("Affect Only Locations", "True and False"),
    ("Affect Only Parents", "True and True"),
    ("Auto IK", "True and False"),
    ("X-Mirror (Relative)", "True and True"),
    ("X-Mirror", "True and False"),
    ("Affect Only Locations", "True and True"),
]


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
    log.header("GenTextLines Test")
    gtl = GenTextLines()
    for text, condition in console_test_data:
        log.info("{}: {}".format(text, gtl.eval(condition)))
    log.header("get_text_lines()")
    log.info(gtl.get_text_lines())
