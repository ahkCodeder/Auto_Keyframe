import bpy
from . import main


class DATA_OT_DS_Auto_Key(bpy.types.Operator):

    bl_idname = "data.auto_key"
    bl_label = "Auto Key"
    bl_options = {'REGISTER', 'UNDO'}

    MODE: bpy.props.EnumProperty(items=[
        ("SELECTION", "SELECTION", ""),
        ("SPACEING", "SPACEING", ""),
        ("MOVE", "MOVE", ""),
        ("EASING", "EASING", "")])

    amount: bpy.props.IntProperty(
        name="amount",
        description="amount to do on the frames where it might mean space etc",
        default=1,
        min=-2000,
        max=2000)

    end_frame: bpy.props.IntProperty(
        name="end frame",
        description="sets the last frame  ",
        default=1,
        min=-2000000,
        max=2000000)

    force_all_constant_spaceing: bpy.props.BoolProperty(
        name="constant spaceing",
        description="this forces the spaceing between frames to be constant",
        default=False)

    @classmethod
    def poll(cls, context):

        area_type = "DOPESHEET_EDITOR"
        for area in bpy.context.screen.areas:
            if area.type == area_type:
                return True

        return False

    # SIMPLE JUST RUNS SOMETHING
    def execute(self, context):

        if self.poll(self):

            main.main(MODE=self.MODE, amount=self.amount,
                      end_frame=self.end_frame,
                      is_force_spaceing=self.force_all_constant_spaceing)

            return {'FINISHED'}

        return {'CANCELED'}


def register():

    bpy.utils.register_class(DATA_OT_DS_Auto_Key)


def unregister():

    bpy.utils.unregister_class(DATA_OT_DS_Auto_Key)


if __name__ == "__main__":
    register()
