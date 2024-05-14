import bpy

"""
INSTRUCTION 

YOU NEED TO HAVE DOPE SHEET OPEN
"""


def main(MODE="", amount=0, end_frame=0, is_force_spaceing=True, interpolation_list=[""], interpolation_mode=""):

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

    elif MODE == "AUTO_INTERPOLATION":
        interpolation(context_override,amount, interpolation_list, interpolation_mode)


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
            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                bpy.ops.action.select_column(mode='CFRA')
            count = 0

        else:
            count += 1
        ret = bpy.ops.screen.keyframe_jump(next=True)

        if {'CANCELLED'} == ret:
            break


def move(move_amount, context_override):

    if move_amount != 0:
        with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
            bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                    orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=move_amount,
                                    use_proportional_connected=False, use_proportional_projected=False)


def spaceing(spaceing_amount, end_frame, context_override):
    steps = 1
    if spaceing_amount != 0:
        start_frame = bpy.data.scenes[0].frame_current

        with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
            bpy.ops.action.select_all(action='DESELECT')

        if spaceing_amount < 0:
            steps = count_steps(
                0, False, start_frame=start_frame, end_frame=end_frame) + 1
            step = 0

            bpy.data.scenes[0].frame_current = start_frame

            while True:
                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.select_column(mode='CFRA')

                    bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(spaceing_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                            orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                                            use_proportional_connected=False, use_proportional_projected=False)

                bpy.data.scenes[0].frame_current = bpy.data.scenes[0].frame_current + \
                    spaceing_amount
                ret = bpy.ops.screen.keyframe_jump(next=False)

                if ret == {'CANCELLED'} or bpy.data.scenes[0].frame_current <= end_frame:
                    break

            bpy.data.scenes[0].frame_current = start_frame

            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                bpy.ops.action.select_all(action='DESELECT')

            while True:
                ret = bpy.ops.screen.keyframe_jump(next=True)
                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.select_column(mode='CFRA')

                if ret == {'CANCELLED'}:
                    break

            move_amount = spaceing_amount*steps

            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1,
                                        use_proportional_connected=False, use_proportional_projected=False)

        else:
            steps = count_steps(
                0, True, start_frame=start_frame, end_frame=end_frame) + 1
            step = 0

            bpy.data.scenes[0].frame_current = end_frame

            while True:
                ret = bpy.ops.screen.keyframe_jump(next=True)

                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.select_column(mode='CFRA')

                if ret == {'CANCELLED'}:
                    break

            move_amount = spaceing_amount*steps-spaceing_amount

            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=move_amount,
                                        use_proportional_connected=False, use_proportional_projected=False)

                bpy.ops.action.select_all(action='DESELECT')

            bpy.data.scenes[0].frame_current = end_frame

            bpy.ops.screen.keyframe_jump(next=False)

            bpy.ops.screen.keyframe_jump(next=True)

            if bpy.data.scenes[0].frame_current != end_frame:
                bpy.ops.screen.keyframe_jump(next=False)

            while True:
                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.select_column(mode='CFRA')

                current_frame = bpy.data.scenes[0].frame_current

                reposition = spaceing_amount*(steps - step - 1)

                bpy.data.scenes[0].frame_current = current_frame + reposition

                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.snap(type='CFRA')

                ret = bpy.ops.screen.keyframe_jump(next=False)

                if {'CANCELLED'} == ret or start_frame > bpy.data.scenes[0].frame_current:
                    break

                step += 1

                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.select_all(action='DESELECT')


def force_all_constant_spaceing(force_amount, context_override):
    if force_amount != 0:
        with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
            bpy.ops.action.select_all(action='DESELECT')

        start_frame = bpy.data.scenes[0].frame_current

        while True:
            current_frame = bpy.data.scenes[0].frame_current

            ret = bpy.ops.screen.keyframe_jump(next=True)

            next_frame_index = bpy.data.scenes[0].frame_current

            if (next_frame_index - current_frame) != force_amount:
                move_amount = -1 * \
                    ((next_frame_index - current_frame) - force_amount)

            while True:
                with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                    bpy.ops.action.select_column(mode='CFRA')
                ret = bpy.ops.screen.keyframe_jump(next=True)

                if ret == {'CANCELLED'}:
                    break

            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                #! TODO :: check if the force amount works
                bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(move_amount, 0, 0, 0), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                        orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=move_amount,
                                        use_proportional_connected=False, use_proportional_projected=False)

            bpy.data.scenes[0].frame_current = current_frame + force_amount

            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                bpy.ops.action.select_all(action='DESELECT')

            ret = bpy.ops.screen.keyframe_jump(next=True)

            if ret == {'CANCELLED'}:
                break

            bpy.ops.screen.keyframe_jump(next=False)

        bpy.data.scenes[0].frame_current = start_frame


def interpolation(context_override,keyframe_gap_amount, interpolation_list, interpolation_mode, on_selected=False):

    seleted_keyframes = []
    # This adds the selected keyframs to a list
    if on_selected:
        for f in bpy.context.object.animation_data.action.fcurves:
            for key_frame in f.keyframe_points:
                if key_frame.select_control_point:
                    if not int(key_frame.co[0]) in seleted_keyframes:
                        seleted_keyframes.append(int(key_frame.co[0]))

    if len(seleted_keyframes) > 0:

        bpy.ops.action.select_all(action='DESELECT')

        for index, keyframe_index in enumerate(seleted_keyframes):
            bpy.data.scenes[0].frame_current = keyframe_index
            with bpy.context.temp_override(window=context_override['window'],area=context_override['area'],region=context_override['region']):
                bpy.ops.action.select_column(mode='CFRA')

            # !START :: test and then refactor for multiples and diffrent modes
            step = len(interpolation_list) % index
            bpy.ops.action.interpolation_type(type=interpolation_list[step])

    else:
        print()

    # TODO :: apply the frames on the list iwth the array and mode needed
    if len(interpolation_list) == 1:
        #! TODO :: FIX THE ZERO ISSUE 
        selection(keyframe_gap_amount,0,context_override)
    else:
        print()

# TODO :: MAKE A MODE CALLED AUTO_PUSH_KEY_FRAMES each time you amke a key frame move on an object you skipp a certain amount of frames forward to make the key frameing faster 
# TODO :: CORPRATE CUSTOM PATTERS THAT CAN BE SAVE AKA STUFF THAT OFTHEN HAPPENS LIKE A CERANT SEQUENS OF ARRAYS AND KEY FRAMES SELECTED SO THAT YOU CAN AUTOMATE EVEN FASTER
# TODO :: MAKE CUSTOME EASING TYPES
    # TODO :: STEPS CONSTAT BUT WITH UP OR STEP DOWN AND OTHER EASING TYPES
# TODO :: CREATE NEW DYNAMIC EFFECTS SINE WAVE EDITABLE AMPLITUTED AND FREQANSY AND OFF SET HOWEVER THIS MIGHT ALREADY BE AVALABLE SO CHECK IN BLENDER WITH THE WAVE MODIFIER

# TODO :: ADD COSTUME LOGOS
# TODO :: MAKE A SAVE POINT FOR THE KEY FRAMES
