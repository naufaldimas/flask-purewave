from flask import Flask, request, send_file, jsonify
import os
from enhance import purewave_enhance
from flask_cors import CORS

app = Flask(__name__)

# Allow multiple origins
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:8080"]
    }
})

INPUT_PATH = 'audio/dry/'
OUTPUT_PATH = 'audio/wet/'
os.makedirs(INPUT_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

@app.route('/audio', methods=['POST'])
def enhance_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    # Save the uploaded file
    input_path = os.path.join(INPUT_PATH, audio_file.filename)
    audio_file.save(input_path)

    # Call the enhancement function
    enhanced_audio_buffer = purewave_enhance(input_path)
    if isinstance(enhanced_audio_buffer, dict):  # Check if the function returned an error
        return jsonify(enhanced_audio_buffer[0]), enhanced_audio_buffer[1]

    # Save the enhanced audio to a file
    output_path = os.path.join(OUTPUT_PATH, audio_file.filename)
    with open(output_path, 'wb') as f:
        f.write(enhanced_audio_buffer.getvalue())

    # Reset buffer position to allow serving the file
    enhanced_audio_buffer.seek(0)

    # Return the enhanced audio as a downloadable file
    return send_file(
        enhanced_audio_buffer,
        mimetype='audio/wav',
        as_attachment=True,
        download_name = audio_file.filename + ' (enhanced).wav'
    )


@app.route('/audio/<filename>', methods=['GET'])
def download_audio(filename):
    output_path = os.path.join(OUTPUT_PATH, filename)

    if not os.path.exists(output_path):
        return jsonify({"error": "File not found."}), 404

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
