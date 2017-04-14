from flask import Flask, render_template, jsonify
from goprocam import GoProCamera, constants

app = Flask(__name__)
gopro = GoProCamera.GoPro()

gopro_media=gopro.listMedia(True, True)
def format_media(media):
    data = []
    for m in media:
        duration=gopro.parse_value("media_size",int(m[2]))
        if m[1].endswith(".MP4"):
            duration=gopro.parse_value("video_left",int(gopro.getVideoInfo("dur",m[1],m[0])))
        resultData = {'folder': m[0],
                      'filename': m[1],
					  'dur': duration,
                      'purl': "http://10.5.5.9/gp/gpMediaMetadata?p=/" + m[0] + "/" + m[1]}
        data.append(resultData)
    return data	
def gp_info():
	info = ""
	info = info + " " + gopro.infoCamera("model_name")
	info = info + " " + gopro.infoCamera("ap_ssid")
	info = info + " " + gopro.infoCamera("firmware_version")
	info = info + " " + gopro.parse_value("mode", gopro.getStatus(constants.Status.Status, constants.Status.STATUS.Mode))
	info = info + " " + gopro.parse_value("sub_mode", gopro.getStatus(constants.Status.Status, constants.Status.STATUS.SubMode))
	return info
@app.route('/')
def media():
    searchResults = format_media(gopro_media)
    return render_template('index.html', searchResults=searchResults,goproinfo=gp_info())

if __name__ == '__main__':
    app.run(debug=True)