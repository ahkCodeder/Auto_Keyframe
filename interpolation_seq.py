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
