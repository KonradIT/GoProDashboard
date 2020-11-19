# GoProDashboard

A Python webapp to interface with GoPro cameras over USB (GoPro Connect mode/Webcam mode). 

Currently supports viewing media

This project was born out of a necessity to offload media via WiFi while on a trip due to a broken SD card reader.

4 years later, GoPro introduced a mode that allows gpControl APIs to be used using USB Ethernet, thus giving us the APIs necessary to index, download and delete media from the camera programmatically.

![](https://i.imgur.com/u6MBty4.jpg)

### Running:

Plug your GoPro camera, make sure it's in GoPro Connect mode, and wait a few seconds for the RNDIS lease to occur.

````
pipenv shell
python main.py
````

### Configuring:

- `MEDIA_DOWNLOAD_DIR`: this is where the media will be downloaded
- `INTERFACE`: GoPro USB Ethernet interface (run ifconfig if you're not sure)
- `DEBUG`

.env.example provides default values, code will look for .env

### Running GoPro Dashboard automatically when the camera is plugged in

Copy `00-gopro-dashboard` to `/etc/NetworkManager/dispatcher.d`, make the necessary changes to detect the GoPro USB Ethernet interface as well as the path to this repository.

Also, create a file called gopro.dashboard with `enabled` or `disabled` in it to enable/disable starting this program when the camera is plugged in.