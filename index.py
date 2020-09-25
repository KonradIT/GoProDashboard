from flask import Flask, render_template, jsonify
from flask import request
from goprocam import GoProCamera, constants

app = Flask(__name__)
gopro = GoProCamera.GoPro(ip_address=GoProCamera.GoPro.getWebcamIP("enp0s20u2"), camera=constants.gpcontrol, webcam_device="enp0s20u2")
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
    searchResults = format_media()
    return render_template('index.html', searchResults=searchResults,goproinfo=gp_info())

@app.route('/delete')
def delete_media():
	gopro.deleteFile(request.args.get('folder'),request.args.get('filename'))
	return media()
if __name__ == '__main__':
    app.run(debug=True)