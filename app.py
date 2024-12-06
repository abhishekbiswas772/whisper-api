from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)
model = whisper.load_model("tiny")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # Ensure a file is provided in the request
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)

        # Perform transcription with timestamps
        result = model.transcribe(audio, task="transcribe")
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],  # Start time in seconds
                "end": segment["end"],      # End time in seconds
                "text": segment["text"]     # Transcribed text
            })
        return jsonify({
            "language": result["language"],
            "segments": segments
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
