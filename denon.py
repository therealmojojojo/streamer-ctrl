# denon.py

import denonavr
import logging

logger = logging.getLogger('streamer_ctrl_logger')

class Denon:
    def __init__(self, ip_address):
        self.avr = denonavr.DenonAVR(ip_address)
        self.ip_address = ip_address
        self.was_started = False

    def power_on(self):
        self.update_status()
        self.avr.power_on()

    def power_off(self):
        self.update_status()
        self.avr.power_off()

    def update_status(self):
        """ Update the status of the AVR from the device. """
        self.avr.update()

    def set_power_status(self, status):
        """ Get the power status of the AVR. """
        self.update_status()
        if status == "ON":
          self.power_on()
        else:
          self.power_off()
        return self.avr.power

    def get_power_status(self):
        """ Get the power status of the AVR. """
        self.update_status()
        return self.avr.power

    def get_current_input(self):
        """ Get the current input source of the AVR. """
        self.update_status()
        return self.avr.input_func

    def set_input_source(self, input_source):
        """ Set the AVR to a specified input source. """
        return self.avr.set_input_func(input_source)

    def get_volume_level(self):
        """ Get the current volume level of the AVR. """
        self.update_status()
        return self.avr.volume

    def set_volume_level(self, volume_level):
        """ Set the AVR to a specified volume level. """
        return self.avr.set_volume(volume_level)
    
    def print_status(self):
        logger.info(f"Denon AVR at {self.ip_address} is currently {'ON' if self.get_power_status() == 'ON' else 'OFF'}, "
              f"on input {self.get_current_input()}.")
