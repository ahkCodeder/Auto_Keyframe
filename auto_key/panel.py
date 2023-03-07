import bpy


class VIEW3D_PT_DS_Auto_Key(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Auto Key"
    bl_label = "Auto Key"

    def draw(self, context):

        props = self.layout.operator("data.auto_key", text="Run")

        col = self.layout.column(align=True)

        col.prop(context.scene, 'MODE')

        props.MODE = context.scene.MODE

        if props.MODE == "SELECTION":

            col.prop(context.scene, 'amount')
            col.prop(context.scene, 'end_frame')

            props.amount = context.scene.amount
            props.end_frame = context.scene.end_frame

        elif props.MODE == "SPACEING":

            col.prop(context.scene, 'amount')
            col.prop(context.scene, 'end_frame')
            col.prop(context.scene, 'force_all_constant_spaceing')

            props.amount = context.scene.amount
            props.end_frame = context.scene.end_frame
            props.force_all_constant_spaceing = context.scene.force_all_constant_spaceing

        elif props.MODE == "MOVE":

            col.prop(context.scene, 'amount')

            props.amount = context.scene.amount

        elif props.MODE == "EASING":

            col.prop(context.scene, 'amount')

            props.amount = context.scene.amount


def register():

    bpy.types.Scene.MODE = bpy.props.EnumProperty(items=[
        ("SELECTION", "SELECTION", ""),
        ("SPACEING", "SPACEING", ""),
        ("MOVE", "MOVE", ""),
        ("EASING", "EASING", "")])

    bpy.types.Scene.end_frame = bpy.props.IntProperty(
        name="end frame",
        description="this sets the end frame for the mode given",
        default=1,
        min=-2000000,
        max=2000000)

    bpy.types.Scene.amount = bpy.props.IntProperty(
        name="frame amount",
        description="the amount of frames",
        default=1,
        min=-2000,
        max=2000)

    bpy.types.Scene.force_all_constant_spaceing = bpy.props.BoolProperty(
        name="force all constant spaceing",
        description="this forces the spaceing of the frames to be constant",
        default=False)

    bpy.utils.register_class(VIEW3D_PT_DS_Auto_Key)


def unregister():

    del bpy.types.Scene.MODE

    del bpy.types.Scene.end_frame

    del bpy.types.Scene.amount

    del bpy.types.Scene.force_all_constant_spaceing

    bpy.utils.unregister_class(VIEW3D_PT_DS_Auto_Key)


if __name__ == "__main__":
    register()
