from flask import Flask, render_template, request, jsonify
from models import triage_case, detect_emotion, generate_legal_document
from database import save_complaint, get_complaint_status
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    data = request.json
    complaint_text = data.get('complaint', '')

    if not complaint_text:
        return jsonify({"error": "Complaint text is required"}), 400

    # Triage the case
    try:
        triage_response = triage_case(complaint_text)
        emotion = detect_emotion(complaint_text)
        document = generate_legal_document(complaint_text)
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500
    
    # Save complaint to the database
    complaint_data = {
        "complaint_text": complaint_text,
        "triage_response": triage_response,
        "emotion_detected": emotion,
        "generated_document": document,
        "status": "Submitted"
    }
    try:
        result = save_complaint(complaint_data)
        complaint_id = str(result)
    except Exception as e:
        return jsonify({"error": f"Error saving complaint: {str(e)}"}), 500
    
    return jsonify({
        "message": "Complaint submitted successfully",
        "triage_response": triage_response,
        "emotion_detected": emotion,
        "generated_document": document,
        "complaint_id": complaint_id
    })

@app.route('/check_status/<complaint_id>', methods=['GET'])
def check_status(complaint_id):
    try:
        complaint_id = ObjectId(complaint_id)
    except Exception:
        return jsonify({"error": "Invalid complaint ID format"}), 400

    status = get_complaint_status(complaint_id)
    if status:
        return jsonify({
            "complaint_id": str(complaint_id),
            "status": status
        })
    else:
        return jsonify({"error": "Complaint not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
