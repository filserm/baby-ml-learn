from phue import Bridge
import time


class Light():

    def __init__(self):
        self.b = Bridge('192.168.0.22')

        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        self.b.connect()

        # Get the bridge state (This returns the full dictionary that you can explore)
        #self.b.get_api()

        # Get a flat list of the light objects (same as calling b.lights)
        self.lights_list = self.b.get_light_objects('list')


    def turnon_light(self, dim=127):
        for light in self.lights_list:
            if 'Lidl' in light.name:
                light.on = True
                light.brightness = dim
                dim_state = dim
                return light, dim_state

    def turnoff_light(self):
        for light in self.lights_list:
            if 'Lidl' in light.name:
                light.on = False

    def brightness_up(self, dim_state=0):    
        while dim_state <= 254:
            light.brightness = dim_state
            time.sleep(3)
            dim_state+=10


if __name__ == '__main__':
    l = Light()
    light, dim_state = l.turnon_light(dim=5)
    l.brightness_up(dim_state=dim_state)
    time.sleep(20)
    l.turnoff_light()