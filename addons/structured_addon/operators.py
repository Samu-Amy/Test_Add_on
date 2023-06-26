import bpy
import random


def add_random_location(objects, amount=1, do_axis=(True, True, True)):

    for ob in objects:
        for i in range(3):
            if do_axis[i]:
                loc = ob.location
                loc[i] += random.randint(-amount, amount)


class TRANSFORM_OT_random_location(bpy.types.Operator):
    bl_idname = "transfrom.add_random_location"
    bl_label = "Add random Location"

    amount: bpy.props.IntProperty(name="Amount", default=1)
    axis: bpy.props.BoolVectorProperty(
        name="Displace Axis", default=(True, True, True))

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        add_random_location(context.selected_objects, self.amount, self.axis)
        return {"FINISHED"}


class ANIMATION_OT_action_to_scene_range(bpy.types.Operator):
    """Set Playback range to current action Start/End"""
    bl_idname = "anim.action_to_range"
    bl_label = "Action Range to Scene"
    bl_description = "Transfer action range ro scene range"
    bl_options = {"REGISTER", "UNDO"}

    use_preview: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        obj = context.object
        if not obj:
            return False
        if not obj.animation_data:
            return False
        if not obj.animation_data.action:
            return False
        return True

    def execute(self, context):
        anim_data = context.object.animation_data
        first, last = anim_data.action.frame_range


def register_classes():
    bpy.utils.register_class(TRANSFORM_OT_random_location)


def unregister_classes():
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)
