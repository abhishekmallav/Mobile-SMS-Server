from jnius import autoclass, cast

def toggle_android_flashlight(state: bool):
    try:
        # Load required Android classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        
        # Get the camera manager service
        activity = PythonActivity.mActivity
        camera_manager = cast('android.hardware.camera2.CameraManager', 
                              activity.getSystemService(Context.CAMERA_SERVICE))
        
        # Usually, the back camera with the flashlight is the first one (id '0')
        camera_id = camera_manager.getCameraIdList()[0]
        
        # Turn it on or off
        camera_manager.setTorchMode(camera_id, state)
        return True, f"Flashlight turned {'on' if state else 'off'}"
    except Exception as e:
        return False, str(e)