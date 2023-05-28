from . import panel,operator

bl_info = {
    "name": "Auto Key",
    "author": "AHK <https://github.com/ahkCodeder>",
    "version": (1, 1),
    "blender": (3, 4, 0),
    "category": "3D View",
    "location": "View3D",
    "description": "This trys to automate parts of keyframe selection and other aspects of keyframes and animations",
    "warning": "",
    "doc_url": "https://github.com/ahkCodeder/Auto_Keyframe"
}

classes = [panel, operator]


def register():

    for c in classes:
        c.register()


def unregister():

    for c in classes:
        c.unregister()


if __name__ == "__main__":
    register()
