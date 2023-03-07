import bpy

"""
INSTRUCTION 

YOU NEED TO HAVE DOPE SHEET OPEN
"""


def main(MODE="", amount=0, end_frame=0, is_force_spaceing=True):

    context_override = context_swap("DOPESHEET_EDITOR")

    if MODE == "SPACEING" and is_force_spaceing:

        force_all_constant_spaceing(
            force_amount=amount, context_override=context_override)

    elif MODE == "SPACEING":

        spaceing(spaceing_amount=amount, end_frame=end_frame,
                 context_override=context_override)

    elif MODE == "SELECTION":

        selection(offset_amount=amount, end_frame=end_frame,
                  context_override=context_override)

    elif MODE == "MOVE":

        move(move_amount=amount, context_override=context_override)

    elif MODE == "EASING":
        # TODO :: ADD FUNC CALL
        print("NOT DIFEIND YET")


def count_steps(steps, isPositive, start_frame, end_frame):

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
        # TODO :: ADD ERR HANDLE
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


def selection(offset_amount, end_frame, context_override):
    count = offset_amount

    while True:
        if end_frame < bpy.data.scenes[0].frame_current:
            break

        if count == offset_amount:
            bpy.ops.action.select_column(context_override, mode='CFRA')
            count = 0

        else:
            count += 1
        ret = bpy.ops.screen.keyframe_jump(next=True)

        if {'CANCELLED'} == ret:
            break


def move(move_amount, context_override):

    if move_amount != 0:
        bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                    orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=move_amount,
                                    use_proportional_connected=False, use_proportional_projected=False)


def spaceing(spaceing_amount, end_frame, context_override):
    steps = 1
    if spaceing_amount != 0:
        start_frame = bpy.data.scenes[0].frame_current

        bpy.ops.action.select_all(context_override, action='DESELECT')

        if spaceing_amount < 0:
            steps = count_steps(
                0, False, start_frame=start_frame, end_frame=end_frame) + 1
            step = 0

            bpy.data.scenes[0].frame_current = start_frame

            while True:
                bpy.ops.action.select_column(context_override, mode='CFRA')

                bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(spaceing_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                            orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                                            use_proportional_connected=False, use_proportional_projected=False)

                bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + \
                    spaceing_amount
                ret = bpy.ops.screen.keyframe_jump(next=False)

                if ret == {'CANCELLED'} or bpy.data.scenes[0].frame_current <= end_frame:
                    break

            bpy.data.scenes[0].frame_current = start_frame

            bpy.ops.action.select_all(context_override, action='DESELECT')

            while True:
                ret = bpy.ops.screen.keyframe_jump(next=True)
                bpy.ops.action.select_column(context_override, mode='CFRA')

                if ret == {'CANCELLED'}:
                    break

            move_amount = spaceing_amount*steps

            bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                                        use_proportional_connected=False, use_proportional_projected=False)

        else:
            steps = count_steps(
                0, True, start_frame=start_frame, end_frame=end_frame) + 1
            step = 0

            bpy.data.scenes[0].frame_current = end_frame

            while True:
                ret = bpy.ops.screen.keyframe_jump(next=True)

                bpy.ops.action.select_column(context_override, mode='CFRA')

                if ret == {'CANCELLED'}:
                    break

            move_amount = spaceing_amount*steps-spaceing_amount

            bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=move_amount,
                                        use_proportional_connected=False, use_proportional_projected=False)

            bpy.ops.action.select_all(context_override, action='DESELECT')

            bpy.data.scenes[0].frame_current = end_frame

            bpy.ops.screen.keyframe_jump(next=False)

            bpy.ops.screen.keyframe_jump(next=True)

            if bpy.data.scenes[0].frame_current != end_frame:
                bpy.ops.screen.keyframe_jump(next=False)

            while True:
                bpy.ops.action.select_column(context_override, mode='CFRA')

                current_frame = bpy.data.scenes[0].frame_current

                reposition = spaceing_amount*(steps - step - 1)

                bpy.data.scenes[0].frame_current = current_frame + reposition

                bpy.ops.action.snap(context_override, type='CFRA')

                ret = bpy.ops.screen.keyframe_jump(next=False)

                if {'CANCELLED'} == ret or start_frame > bpy.data.scenes[0].frame_current:
                    break

                step += 1

                bpy.ops.action.select_all(context_override, action='DESELECT')


def force_all_constant_spaceing(force_amount, context_override):
    if force_amount != 0:
        bpy.ops.action.select_all(context_override, action='DESELECT')

        start_frame = bpy.data.scenes[0].frame_current

        while True:
            current_frame = bpy.data.scenes[0].frame_current

            ret = bpy.ops.screen.keyframe_jump(next=True)

            next_frame_index = bpy.data.scenes[0].frame_current

            if (next_frame_index - current_frame) != force_amount:
                move_amount = -1 * \
                    ((next_frame_index - current_frame) - force_amount)

            while True:
                bpy.ops.action.select_column(context_override, mode='CFRA')
                ret = bpy.ops.screen.keyframe_jump(next=True)

                if ret == {'CANCELLED'}:
                    break

            bpy.ops.transform.transform(context_override, mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=move_amount,
                                        use_proportional_connected=False, use_proportional_projected=False)

            bpy.data.scenes[0].frame_current = current_frame + force_amount

            bpy.ops.action.select_all(context_override, action='DESELECT')

            ret = bpy.ops.screen.keyframe_jump(next=True)

            if ret == {'CANCELLED'}:
                break

            bpy.ops.screen.keyframe_jump(next=False)

        bpy.data.scenes[0].frame_current = start_frame

# TODO :: START HERE :: TEST THAT IT WORKS FOR ALL MODES -> UPLOAD UPDATE
# TODO :: AUTOMATE APPLYING INTEPOLATION TYPE USE DATA FROM SELECTION AND APPLY ON THE GAPS OF CONNECTED OR GAPS

# !INFO :: it dosnt work for key frames that are spased but for key frames that are SOLOS, and there are ADV SETTINGS TO SCLE MORE THEN JUST POSITOIN SCALE ROTATION AND LOCATION CAN BE ANIPULATED

# IDEAR :: BY DEFUALT ONLY MANIPULAT THE ONCE THAT CHANGE THEN AD AN ADV SETTING

# TODO :: MAKE CUSTOME EASING TYPES
    # TODO :: STEPS CONSTAT BUT WITH UP OR STEP DOWN AND OTHER EASING TYPES
# TODO :: CREATE NEW DYNAMIC EFFECTS SINE WAVE EDITABLE AMPLITUTED AND FREQANSY AND OFF SET HOWEVER THIS MIGHT ALREADY BE AVALABLE SO CHECK IN BLENDER WITH THE WAVE MODIFIER

# TODO :: ADD COSTUME LOGOS
# TODO :: MAKE A SAVE POINT FOR THE KEY FRAMES
