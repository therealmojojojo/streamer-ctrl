# streamer-ctrl
Controller for helping with listening music. 
## Usecases:  

1. all devices off, start streaming music via Node => AVR starts, sets itself on the right input and starts playing music from the start
2. AVR is already started, input set on TV playing channel (PS, Apple TV...). Start streaming => AVR changes to the right input and plays the streamed audio
3. Streaming is stopped/paused for more than 10 minutes. => automatically stops AVR
4. AVR is switched to TV => streamer is automatically stopped. 
5. the script installed on ubuntu, continuously monitoring the devices. 

# Devices
- AVR x2300w
- LG Oled TV
- Bluesound Node N130 streamer

# Documentation
- denonavr python library - https://github.com/ol-iver/denonavr
- Bluesound API (HTTP/XML based) - https://github.com/superfell/BluShepherd/blob/master/api.md

