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
        scn = context.scene

        if self.use_preview:
            scn.frame_preview_start = int(first)
            scn.frame_preview_end = int(last)
        else:
            scn.frame_start = int(first)
            scn.frame_end = int(last)

        try:
            bpy.ops.action.view_all()
        except RuntimeError:
            for window in context.window_manager.window:
                screen = window.screen

                for area in screen.areas:
                    if area.type != "DOPESHEET_EDITOR":
                        for region in area.regions:
                            if region.type == "WINDOW":
                                with context.temp_override(window=window, area=area, region=region):
                                    bpy.ops.action.view_all()
                                break
                            break
                        break

        return {"FINISHED"}
    

def view_menu_items(self, context):
    props = self.layout.operator(ANIMATION_OT_action_to_scene_range.bl_idname, text=ANIMATION_OT_action_to_scene_range.bl_label + " (preview)")
    props.use_preview = True

    props = self.layout.operator(ANIMATION_OT_action_to_scene_range.bl_idname, text=ANIMATION_OT_action_to_scene_range.bl_label)
    props.use_preview = False


def register_classes():
    bpy.utils.register_class(TRANSFORM_OT_random_location)
    bpy.utils.register_class(ANIMATION_OT_action_to_scene_range)
    bpy.types.TIME_MT_view.append(view_menu_items)


def unregister_classes():
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)
    bpy.utils.unregister_class(ANIMATION_OT_action_to_scene_range)
    bpy.types.TIME_MT_view.remove(view_menu_items)
