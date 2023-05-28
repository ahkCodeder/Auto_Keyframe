import bpy


class INTERPOLATION_SEQ_OT_NewItem(bpy.types.Operator):
    """Add a new item to the list."""

    bl_idname = "interpolation_seq.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        context.scene.interpolation_seq.add()

        return {'FINISHED'}


class INTERPOLATION_SEQ_OT_DeleteItem(bpy.types.Operator):
    """Delete the selected item from the list."""

    bl_idname = "interpolation_seq.delete_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.interpolation_seq

    def execute(self, context):
        interpolation_seq = context.scene.interpolation_seq
        index = context.scene.list_index

        interpolation_seq.remove(index)
        context.scene.list_index = min(
            max(0, index - 1), len(interpolation_seq) - 1)

        return {'FINISHED'}


class ListItem(bpy.types.PropertyGroup):
    """Group of properties representing an item in the list."""

    name: bpy.props.EnumProperty(
        items=[('CONSTANT', 'CONSTANT', ''), ('LINEAR', 'LINEAR', ''),
               ('BEZIER', 'BEZIER', ''), ('SINE', 'SINE', ''),
               ('QUAD', 'QUAD', ''), ('CUBIC', 'CUBIC', ''),
               ('QUART', 'QUART', ''), ('QUINT', 'QUINT', ''),
               ('EXPO', 'EXPO', ''), ('CIRC', 'CIRC', ''),
               ('BACK', 'BACK', ''), ('BOUNCE', 'BOUNCE', ''),
               ('ELASTIC', 'ELASTIC', '')])


class INTERPOLATION_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name[0:], icon=("IPO_"+item.name[0:]))

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon="NONE")


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

        elif props.MODE == "AUTO_INTERPOLATION":

            col.prop(context.scene, 'amount')
            col.prop(context.scene, 'on_selected')
            col.prop(context.scene, 'interpolation_mode')

            col.template_list("INTERPOLATION_UL_List", "The_List", context.scene,
                              "interpolation_seq", context.scene, "list_index")

            col.operator('interpolation_seq.new_item', text='NEW')
            col.operator('interpolation_seq.delete_item', text='REMOVE')

            if context.scene.list_index >= 0 and context.scene.interpolation_seq:
                item = context.scene.interpolation_seq[context.scene.list_index]
                col.prop(item, "name")

            seq_list = ""

            for interpolation in context.scene.interpolation_seq:
                seq_list += interpolation.name + ","

            props.amount = context.scene.amount
            props.on_selected = context.scene.on_selected
            props.interpolation_mode = context.scene.interpolation_mode
            props.interpolation_seq = seq_list


def register():

    bpy.utils.register_class(INTERPOLATION_SEQ_OT_NewItem)
    bpy.utils.register_class(INTERPOLATION_SEQ_OT_DeleteItem)

    bpy.types.Scene.MODE = bpy.props.EnumProperty(items=[
        ("SELECTION", "SELECTION", ""),
        ("SPACEING", "SPACEING", ""),
        ("MOVE", "MOVE", ""),
        ("AUTO_INTERPOLATION", "AUTO_INTERPOLATION", "")])

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

    bpy.types.Scene.interpolation_mode = bpy.props.EnumProperty(items=[(
        "FORWARD_REAPEAT", "FORWARD_REAPEAT", ""), ("FORWARD_BACKWARD", "FORWARD_BACKWARD", "")])

    bpy.utils.register_class(ListItem)
    bpy.types.Scene.interpolation_seq = bpy.props.CollectionProperty(
        type=ListItem)

    bpy.types.Scene.list_index = bpy.props.IntProperty(name="Index for interpolation_seq",
                                                       default=0)

    bpy.types.Scene.on_selected = bpy.props.BoolProperty(
        name='Use selected Frames', description='This sets if you should use the frames that are selected, or all frames',
        default=False)

    bpy.utils.register_class(INTERPOLATION_UL_List)
    bpy.utils.register_class(VIEW3D_PT_DS_Auto_Key)


def unregister():

    bpy.utils.unregister_class(INTERPOLATION_SEQ_OT_NewItem)
    bpy.utils.unregister_class(INTERPOLATION_SEQ_OT_DeleteItem)

    del bpy.types.Scene.interpolation_seq

    del bpy.types.Scene.list_index

    del bpy.types.Scene.MODE

    del bpy.types.Scene.end_frame

    del bpy.types.Scene.amount

    del bpy.types.Scene.force_all_constant_spaceing

    del bpy.types.Scene.interpolation_mode

    del bpy.types.Scene.on_selected

    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(INTERPOLATION_UL_List)
    bpy.utils.unregister_class(VIEW3D_PT_DS_Auto_Key)


if __name__ == "__main__":
    register()
