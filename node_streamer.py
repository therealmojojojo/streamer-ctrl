# node-streamer.py

import requests
import xml.etree.ElementTree as ET
import time
import logging

logger = logging.getLogger('streamer_ctrl_logger')

class NodeStreamer:
    def __init__(self, ip_address):
        self.base_url = f'http://{ip_address}:11000'
        self.ip_address = ip_address
        self.last_play_time = 0
    
    def _send_request(self, endpoint):
        """ Send a GET request to the specified endpoint and parse the XML response. """
        try:
            response = requests.get(f'{self.base_url}/{endpoint}')
            response.raise_for_status()  # Raises an error for bad status
            # Parse the XML response
            return ET.fromstring(response.content)
        except requests.RequestException as e:
            logger.error(f"Error: {e}")
            return None
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return None

    def get_status(self):
        """ Get the current playback state of the Node streamer. """
        status_xml = self._send_request('Status')
        if status_xml is not None:
            state = status_xml.find('state')
            return state.text if state is not None else 'UNKNOWN'
        return 'UNKNOWN'

    def play(self):
        """ Start playback. """
        self.last_play_time = 0
        return self._send_request('Play')

    def pause(self):
        """ Pause playback. """
        return self._send_request('Pause')

    def stop(self):
        """ Stop playback. """
        return self._send_request('Stop')

    def resume(self):
        """ Resume playback. """
        self.last_play_time = 0
        return self._send_request('Play')


    def get_current_track_time(self):
        """ Get the current track time. """
        now_playing_xml = self._send_request('Play')
        if now_playing_xml is not None:
            secs = now_playing_xml.find('secs')
            return int(secs.text) if secs is not None else 0
        return 0

    def back(self):
        """ Restart the current track. """
        self.last_play_time = 0
        self._send_request('Play?seek=0')
        self._send_request('Play') #needs an explicit Play command after seek
    
    def set_last_play_time(self):  
        self.last_play_time = time.time()
        logger.info(f"Shutdown counter has started at {self.last_play_time}.")

    def print_status(self):
        logger.info(f"NodeStreamer at {self.ip_address} is currently {self.get_status()}.")