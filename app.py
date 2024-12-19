from flask import Flask, render_template, Response, jsonify, request
from datetime import datetime
from utils.video import VideoStream
from utils.detection import ObjectDetector
from utils.config import Config

app = Flask(__name__)
config = Config()
video_stream = VideoStream()
detector = ObjectDetector()


@app.route('/')
def index():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_datetime = datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")

    # Get initial production data
    production_data = detector.get_production_data()
    production_data.update({
        'current_time': current_time,
        'current_datetime': current_datetime
    })

    return render_template('index.html', **production_data)


@app.route('/production_data')
def get_production_data():
    """API endpoint to get latest production data"""
    try:
        data = detector.get_production_data()
        data.update({
            'current_time': datetime.now().strftime("%H:%M:%S"),
            'success': True
        })
        return jsonify(data)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/video_feed')
def video_feed():
    return Response(video_stream.generate_frames(detector),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': 'No video file provided'})

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'success': False, 'error': 'No video file selected'})

    try:
        video_stream.set_test_video(video_file)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
