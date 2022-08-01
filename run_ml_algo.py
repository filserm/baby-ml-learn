import os  

from micmon.audio import AudioDevice
from micmon.model import Model

from modules.play_radiostation import radio

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
        print(prediction)
        
        if prediction == "positive":
            cry.count +=1
        elif prediction == "negative":
            cry.count = 0
            cry.action = 0
        
        if cry.count > 3 and not cry.action == 1:
            cry.action = 1
            #play radio
            radio()

        # Resume recording
        source.resume()


