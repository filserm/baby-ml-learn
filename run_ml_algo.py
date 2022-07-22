import os  

from micmon.audio import AudioDevice
from micmon.model import Model

model_dir = os.path.expanduser('/app/models/sound-detect')
model = Model.load(model_dir)
audio_system = 'alsa'        # Supported: alsa and pulse
audio_device = 'plughw:1,0'  # Get list of recognized input devices with arecord -l

with AudioDevice(audio_system, device=audio_device) as source:
    for sample in source:
        # Pause recording while we process the frame
        source.pause()
        prediction = model.predict(sample)
        print(prediction)
        # Resume recording
        source.resume()
