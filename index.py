from flask import Flask, render_template, jsonify
from flask import request
from goprocam import GoProCamera, constants
from signal import signal, SIGINT
from dotenv import load_dotenv
import threading
import json
import traceback
import os

app = Flask(__name__)
load_dotenv(dotenv_path='.env')

gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP(os.getenv("INTERFACE")), camera=constants.gpcontrol, webcam_device=os.getenv("INTERFACE"))
def handler(s, f):
    try:
        gopro.gpTurbo(constants.off)
    except: pass
    quit()

def format_media():
    media=gopro.listMedia(True, True)
    return media	
def gp_info():
	info = ""
	info = info + " " + gopro.infoCamera("model_name")
	info = info + " " + gopro.infoCamera("ap_ssid")
	info = info + " " + gopro.infoCamera("firmware_version")
	return info
@app.route('/')
def media():
    media = format_media()
    return render_template('index.html', media=media,goproinfo=gp_info(), ip_address=GoProCamera.GoPro.getWebcamIP(os.getenv("INTERFACE")))

@app.route("/ping")
def ping():
    if len(gopro.infoCamera()) == 0:
        return "not ok"
    return "ok"
@app.route("/download")
def download():
    x = threading.Thread(target=gopro.downloadMedia, args=(request.args.get('folder'),request.args.get('filename'), os.getenv("MEDIA_DOWNLOAD_DIR") + "/" + request.args.get('folder') + "_" +request.args.get('filename'),))
    x.start()
    return ("", 200)

@app.route('/delete')
def delete_media():
	gopro.deleteFile(request.args.get('folder'),request.args.get('filename'))
	return media()

if __name__ == '__main__':
    signal(SIGINT, handler)
    gopro.gpTurbo(constants.on)
    app.run(debug=True if os.getenv("DEBUG") == "true" else False)