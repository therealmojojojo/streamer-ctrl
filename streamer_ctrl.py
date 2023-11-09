#!/usr/bin/env python3

import denon
import time
import node_streamer
import logging
from logging.handlers import RotatingFileHandler
import os

# Replace with the IP address of your Denon AVR
AVR_IP_ADDRESS = '192.168.1.193'
STREAMER_IP = "192.168.1.167"
POLL_INTERVAL = 3  # Time in seconds between each status check
WAIT_FOR_AVR_TO_START = 15
WAIT_FOR_AVR_TO_CHANGE_INPUT = 1
AVR_INPUT = 'Media Player'

logger = logging.getLogger('streamer_ctrl_logger')

def init_logging():
    # Define the log file location
    log_file = '/var/log/streamer_ctrl.log'

    # Define the log level
    log_level = logging.INFO

    # Create a logger
    logger = logging.getLogger('streamer_ctrl_logger')
    logger.setLevel(log_level)

    # Create a rotating file handler
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024,  # 10 MB
        backupCount=5
    )

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Set the formatter for the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # To handle the case where the log directory requires root access,
    # you might want to check permissions and warn the user.
    if not os.access(os.path.dirname(log_file), os.W_OK):
        print(f"Warning: The process lacks write permissions for the file {log_file},"
              " logging to '/var/log/' might require root access.")



# Function to manage the logic for NodeStreamer and Denon interaction
def manage_devices(node_streamer: node_streamer.NodeStreamer, denon_avr:denon.Denon, media_player_input=AVR_INPUT):
    while True:
        node_status = node_streamer.get_status()
        denon_power_status = denon_avr.get_power_status()
        denon_current_input = denon_avr.get_current_input()

        # If NodeStreamer is streaming and Denon is stopped, start Denon and set to "Media Player"
        if node_status == "stream" and denon_power_status == 'OFF':
            node_streamer.pause()
            denon_avr.set_power_status('ON')
            time.sleep(WAIT_FOR_AVR_TO_START)
            denon_avr.set_input_source(media_player_input)
            denon_avr.was_started = True
            time.sleep(WAIT_FOR_AVR_TO_CHANGE_INPUT)
            #get back to the beginning of the track
            node_streamer.back()
    

        # If NodeStreamer is streaming and Denon is ON, set the input to "Media Player"
        elif node_status == "stream" and denon_power_status == 'ON':
            if denon_current_input != media_player_input:
                if not denon_avr.was_started:
                    node_streamer.pause()
                    denon_avr.set_input_source(media_player_input)
                    denon_avr.was_started = True
                    time.sleep(WAIT_FOR_AVR_TO_CHANGE_INPUT)
                    node_streamer.back()
                else:
                    # the user has changed the input manually - stop the streamer
                    denon_avr.was_started = False
                    node_streamer.stop()
            else:
                #all good, music should be loud and cool, reset the shutdown counter
                denon_avr.was_started = True
                node_streamer.last_play_time = 0
                

        #if node was stopped while denon was playing on the "Media Player" input
        if node_streamer.last_play_time == 0 and node_status in ['stop', 'pause'] and denon_avr.was_started:
            #start the counter
            node_streamer.set_last_play_time()
        
        # If NodeStreamer is stopped or paused for more than 10 minutes, stop Denon if on "Media Player"
        if node_streamer.last_play_time != 0 and \
            node_status in ['stop', 'pause'] and \
                time.time() - node_streamer.last_play_time > 600:
            if denon_power_status == 'ON' and denon_current_input == media_player_input:
                denon_avr.set_power_status('OFF')
                denon_avr.was_started = False
                print("Denon AVR has been turned off after 10 minutes of inactivity.")

        # Pause for a moment before the next status check
        time.sleep(POLL_INTERVAL)
        denon_avr.print_status()
        node_streamer.print_status()



def main():
    logger.info("Starting")
    denon_avr = denon.Denon(AVR_IP_ADDRESS)
    streamer = node_streamer.NodeStreamer(STREAMER_IP)
    manage_devices(streamer, denon_avr)
    logger.info("Stopping ???")

if __name__ == "__main__":
    init_logging()
    main()