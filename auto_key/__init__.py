from auto_key import operator, panel
bl_info = {
    "name": "Auto Key",
    "author": "AHK <https://github.com/ahkCodeder>",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "category": "3D View",
    "location": "View3D",
    "description": "This trys to automate parts of keyframe selection and other aspects of keyframes and animations",
    "warning": "",
    "doc_url": "https://github.com/ahkCodeder/Auto_Keyframe"
}


def register():

    operator.register()
    panel.register()


def unregister():

    operator.unregister()
    panel.unregister()


if __name__ == "__main__":
    register()
