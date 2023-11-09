import denon
import time
import node_streamer

# Replace with the IP address of your Denon AVR
AVR_IP_ADDRESS = '192.168.1.193'
STREAMER_IP = "192.168.1.167"
POLL_INTERVAL = 10  # Time in seconds between each status check
AVR_INPUT = 'Media Player'

# Function to manage the logic for NodeStreamer and Denon interaction
def manage_devices(node_streamer: node_streamer.NodeStreamer, denon_avr:denon.Denon, media_player_input=AVR_INPUT):
    while True:
        node_status = node_streamer.get_status()
        denon_power_status = denon_avr.get_power_status()
        denon_current_input = denon_avr.get_current_input()

        # If NodeStreamer is streaming and Denon is stopped, start Denon and set to "Media Player"
        if node_status == "stream" and denon_power_status == 'OFF':
            denon_avr.set_power_status('ON')
            denon_avr.set_input_source(media_player_input)
            time.sleep(5)
            node_streamer.back()

        # If NodeStreamer is streaming and Denon is ON, set the input to "Media Player"
        elif node_status == "stream" and denon_power_status == 'ON':
            if denon_current_input != media_player_input:
                # TODO add case when user changes the input while playing. node should be stopped
                denon_avr.set_input_source(media_player_input)
                time.sleep(5)
                node_streamer.back()
            

        # If NodeStreamer is stopped or paused for more than 10 minutes, stop Denon if on "Media Player"
        if (node_status in ['stop', 'pause']) and (time.time() - node_streamer.last_play_time > 600):
            if denon_power_status == 'ON' and denon_current_input == media_player_input:
                denon_avr.set_power_status('OFF')
                print("Denon AVR has been turned off after 10 minutes of inactivity.")

        # Pause for a moment before the next status check
        time.sleep(5)
        denon_avr.print_status()
        streamer.print_status()

denon_avr = denon.Denon(AVR_IP_ADDRESS)
streamer = node_streamer.NodeStreamer(STREAMER_IP)

manage_devices(streamer, denon_avr)

