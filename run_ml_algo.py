import os 
import time 

from micmon.audio import AudioDevice
from micmon.model import Model

from modules.play_radiostation import radio
from modules.activate_ligths import Light

model_dir = os.path.expanduser('models/sound-detect')
model = Model.load(model_dir)
audio_system = 'alsa'        # Supported: alsa and pulse
audio_device = 'plughw:1,0'  # Get list of recognized input devices with arecord -l

class cry():
    pass

with AudioDevice(audio_system, device=audio_device) as source:
    for sample in source:
        # Pause recording while we process the frame
        source.pause()
        prediction = model.predict(sample)
        print(f'"babies crying?: {prediction}')
        
        if prediction == "positive":
            cry.count +=1
        elif prediction == "negative":
            cry.count = 0
            cry.action = 0
        
        if cry.count > 3 and not cry.action == 1:
            cry.action = 1
            #play radio
            #radio()

            #turn on lights
            l = Light()
            light, dim_state = l.turnon_light(dim=5)
            l.brightness_up(dim_state=dim_state)
            time.sleep(20)
            l.turnoff_light()

        # Resume recording
        source.resume()


