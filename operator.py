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
        ("AUTO_INTERPOLATION", "AUTO_INTERPOLATION", "")])

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

    interpolation_mode: bpy.props.EnumProperty(items=[(
        "FORWARD_REAPEAT", "FORWARD_REAPEAT", ""), ("FORWARD_BACKWARD", "FORWARD_BACKWARD", "")])

    interpolation_seq: bpy.props.StringProperty()

    on_selected: bpy.props.BoolProperty(
        name='Use selected Frames', description='This sets if you should use the frames that are selected, or all frames',
        default=False)

    @classmethod
    def poll(cls, context):

        try:
            [area for area in bpy.context.screen.areas if area.type ==
                "DOPESHEET_EDITOR"][0]
        except:
            print("YOU NEED TO HAVE :: DOPESHEET_EDITOR :: AREA OPEN")
            return False

        return True

    # SIMPLE JUST RUNS SOMETHING
    def execute(self, context):

        if self.poll(self):

            interpolation_seq_list = self.interpolation_seq.split(",")[:-1]

            main.main(MODE=self.MODE, amount=self.amount,
                      end_frame=self.end_frame,
                      is_force_spaceing=self.force_all_constant_spaceing,
                      interpolation_list=interpolation_seq_list,
                      interpolation_mode=self.interpolation_mode)

            return {'FINISHED'}

        return {'CANCELED'}


def register():

    bpy.utils.register_class(DATA_OT_DS_Auto_Key)


def unregister():

    bpy.utils.unregister_class(DATA_OT_DS_Auto_Key)


if __name__ == "__main__":
    register()
