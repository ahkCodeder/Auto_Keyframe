import bpy

"""
INSTRUCTION 

YOU NEED TO HAVE DOPE SHEET OPEN
""" 

# THIS SETS THE GAP BETWEEN KEY FRAMES FOR SELECTED OBJECT 0 WILL SELECT ALL 
offset_amount = 1

# MOVES EACH FRAME BY THE AMOUNT
move_amount = 0


# THIS ADDS OR REMOVE SPACE BETWEEN FRAMES
spaceing = -2


force_all_constant_spaceing = 0

# THIS SETS THE STOP FRAME
end_frame = 2

start_frame = bpy.data.scenes[0].frame_current 

def count_steps(steps,isPositive):
    
    bpy.data.scenes[0].frame_current = start_frame  
    
    count_steps = steps

    if isPositive:

        while True: 

            ret = bpy.ops.screen.keyframe_jump(next=True)
            
            if {'CANCELLED'} == ret or end_frame <= bpy.data.scenes[0].frame_current:
                return count_steps
            
            count_steps += 1
    else:
        while True:

            ret = bpy.ops.screen.keyframe_jump(next=False)
            
            if {'CANCELLED'} == ret or end_frame >= bpy.data.scenes[0].frame_current:
                return count_steps
            
            count_steps += 1


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

    if {'CANCELLED'} == ret:
        break
    
if move_amount != 0:
    bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size = move_amount,
                                use_proportional_connected=False, use_proportional_projected=False)

steps = 1
if spaceing != 0:
    
    bpy.data.scenes[0].frame_current = start_frame

    bpy.ops.action.select_all(context_override,action='DESELECT')
    
    if spaceing < 0:
        
        steps = count_steps(0,False) + 1
        step = 0
        
        bpy.data.scenes[0].frame_current = start_frame

        while True:
            
            bpy.ops.action.select_column(context_override,mode='CFRA')

            bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(spaceing, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size = 1,
                                use_proportional_connected=False, use_proportional_projected=False)
            
            
            bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + spaceing
            ret = bpy.ops.screen.keyframe_jump(next=False)

            if ret == {'CANCELLED'} or bpy.data.scenes[0].frame_current <= end_frame:
                break
            
        bpy.data.scenes[0].frame_current = start_frame
        
        bpy.ops.action.select_all(context_override,action='DESELECT')
        
        while True:
            
            ret = bpy.ops.screen.keyframe_jump(next=True)
            bpy.ops.action.select_column(context_override,mode='CFRA')
            
        
            if ret == {'CANCELLED'}:
                break
        
        move_amount = spaceing*steps
        
        bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size = 1,
                                use_proportional_connected=False, use_proportional_projected=False)
        


    else:
        
        steps = count_steps(0,True) + 1               
        step = 0
        
        bpy.data.scenes[0].frame_current = end_frame

        while True:

            ret = bpy.ops.screen.keyframe_jump(next=True)

            bpy.ops.action.select_column(context_override,mode='CFRA')

            if ret == {'CANCELLED'}:
                break
        
        move_amount = spaceing*steps-spaceing

        bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size = move_amount,
                                use_proportional_connected=False, use_proportional_projected=False)

        bpy.ops.action.select_all(context_override,action='DESELECT')

        bpy.data.scenes[0].frame_current = end_frame

        bpy.ops.screen.keyframe_jump(next=False)
        
        bpy.ops.screen.keyframe_jump(next=True)
        
        if bpy.data.scenes[0].frame_current != end_frame:
            bpy.ops.screen.keyframe_jump(next=False)
        
        while True:

            bpy.ops.action.select_column(context_override,mode='CFRA')

            current_frame = bpy.data.scenes[0].frame_current

            reposition = spaceing*(steps - step - 1)
            
            bpy.data.scenes[0].frame_current = current_frame + reposition

            bpy.ops.action.snap(context_override,type='CFRA')

            ret = bpy.ops.screen.keyframe_jump(next=False)

            if {'CANCELLED'} == ret or start_frame > bpy.data.scenes[0].frame_current:
                break
            
            step += 1
            
            bpy.ops.action.select_all(context_override,action='DESELECT')

if force_all_constant_spaceing != 0:
    
    # TODO :: IMPLIMENT STOP POINT

    bpy.ops.action.select_all(context_override,action='DESELECT')
    
    bpy.data.scenes[0].frame_current = start_frame

    while True:

        current_frame = bpy.data.scenes[0].frame_current

        ret = bpy.ops.screen.keyframe_jump(next=True)

        next_frame_index = bpy.data.scenes[0].frame_current
        
        if (next_frame_index - current_frame) != force_all_constant_spaceing:
            
            move_amount = -1*((next_frame_index - current_frame) - force_all_constant_spaceing)

        while True:
            
            bpy.ops.action.select_column(context_override,mode='CFRA')
            ret = bpy.ops.screen.keyframe_jump(next=True)

            if ret == {'CANCELLED'}:
                break 
    
        bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size = move_amount,
                                use_proportional_connected=False, use_proportional_projected=False)

        bpy.data.scenes[0].frame_current = current_frame + force_all_constant_spaceing

        bpy.ops.action.select_all(context_override,action='DESELECT')
        
        ret = bpy.ops.screen.keyframe_jump(next=True)
    

        if ret == {'CANCELLED'}:
            break
        
        bpy.ops.screen.keyframe_jump(next=False)