from flask import Flask, render_template, request, session, jsonify
import websocket
import json
import cv2

from record_tool import record

app = Flask(__name__)
app.secret_key = 'qwert'

@app.route('/')
def index():
    # return 'Hello, World!'
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    outputPath, keyLogPath = record()
    session['outputPath'] = outputPath  # 将 outputPath 存储在 session 中
    return jsonify({"outputPath": outputPath,
                    "keyLogPath": keyLogPath})

@app.route('/analyze', methods=['POST'])
def analyze():
    outputPath = session.get('outputPath')  # 从 session 中获取 outputPath
    keyLogPath = session.get('keyLogPath')
    if not outputPath:
        return jsonify({"error": "No recording found"}), 400

    cap = cv2.VideoCapture(outputPath, keyLogPath)
    # 简单示例：计算视频的总帧数
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return jsonify({"frame_count": frame_count})


if __name__ == '__main__':
    app.run(debug=True)
