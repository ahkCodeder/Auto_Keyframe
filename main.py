import bpy

"""
INSTRUCTION 

YOU NEED TO HAVE DOPE SHEET OPEN
""" 

# THIS SETS THE GAP BETWEEN KEY FRAMES FOR SELECTED OBJECT 0 WILL SELECT ALL 
offset_amount = 1

# THIS SETS THE STOP FRAME
end_frame = 40

def context_swap(area_type=""):

        if area_type == "":
            print("no type given")

        override_context = bpy.context.copy()
        area = [area for area in bpy.context.screen.areas if area.type == area_type][0]
        override_context['window'] = bpy.context.window
        override_context['screen'] = bpy.context.screen
        override_context['area'] = area
        override_context['region'] = area.regions[-1]
        override_context['scene'] = bpy.context.scene
        override_context['space_data'] = area.spaces.active

        return override_context
    
context_override = context_swap("DOPESHEET_EDITOR")

count = offset_amount

while True: 
    
    if end_frame < bpy.data.scenes[0].frame_current:
        break

    if count == offset_amount:
        bpy.ops.action.select_column(context_override,mode='CFRA')
        count = 0
    else:
        count += 1
    ret = bpy.ops.screen.keyframe_jump(next=True)

    if 'CANCELLED' in ret:
        break
    
