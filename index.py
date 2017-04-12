from flask import Flask, render_template, jsonify
from goprocam import GoProCamera

app = Flask(__name__)
gopro = GoProCamera.GoPro()

gopro_media=gopro.listMedia(True, True)
def format_media(media):
    data = []
    for m in media:
		duration=""
		if m[1].endswith(".MP4"):
			duration=gopro.getVideoInfo("dur",m[0],m[1])
        resultData = {'folder': m[0],
                      'filename': m[1],
					  'dur': duration,
                      'purl': "http://10.5.5.9/gp/gpMediaMetadata?p=/" + m[0] + "/" + m[1]}
        data.append(resultData)
    return data	
@app.route('/')
def media():
    searchResults = format_media(gopro_media)
    return render_template('index.html', searchResults=searchResults)

if __name__ == '__main__':
    app.run(debug=True)