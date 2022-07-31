import os  

from micmon.audio import AudioDevice
from micmon.model import Model

from modules.play_radiostation import radio

model_dir = os.path.expanduser('models/sound-detect')
model = Model.load(model_dir)
audio_system = 'alsa'        # Supported: alsa and pulse
audio_device = 'plughw:1,0'  # Get list of recognized input devices with arecord -l

with AudioDevice(audio_system, device=audio_device) as source:
    for sample in source:
        # Pause recording while we process the frame
        source.pause()
        prediction = model.predict(sample)
        print(prediction)
        #play radio
        radio()
        # Resume recording
        source.resume()


