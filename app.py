from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import cv2
import numpy as np
import mediapipe as mp
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)
# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

@app.route("/")
def home():
    return "Server is running! ✅"

@app.route("/test")
def test():
    return jsonify({"message": "Server working!", "success": True})

@app.route("/sign-to-text", methods=["POST"])
def sign_to_text():
    try:
        print("📸 Received sign language request")
        
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received", "success": False}), 400
            
        if 'image_data' not in data:
            return jsonify({"error": "No image_data in request", "success": False}), 400

        # Get image data
        image_data = data['image_data']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        print(f"📊 Image data length: {len(image_data)}")

        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data)
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is None:
                return jsonify({"error": "Could not decode image", "success": False}), 400
                
            print(f"🖼️ Image shape: {image.shape}")
            
        except Exception as decode_error:
            print(f"❌ Image decode error: {decode_error}")
            return jsonify({"error": f"Image decode failed: {str(decode_error)}", "success": False}), 400

        # Convert to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process with MediaPipe
        try:
            results = hands.process(rgb_image)
            hands_detected = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0
            print(f"👋 Hands detected: {hands_detected}")
            
        except Exception as mp_error:
            print(f"❌ MediaPipe error: {mp_error}")
            return jsonify({"error": f"MediaPipe processing failed: {str(mp_error)}", "success": False}), 500

        # Simple hand gesture recognition
        if hands_detected > 0:
            # Basic gesture detection
            gestures = []
            for hand_landmarks in results.multi_hand_landmarks:
                # Convert landmarks to simple list
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.append([landmark.x, landmark.y, landmark.z])
                
                # Simple finger counting
                gesture = count_fingers(landmarks)
                gestures.append(gesture)
            
            detected_text = " | ".join(gestures)
        else:
            detected_text = "No hands detected"

        response = {
            "text": detected_text,
            "success": True,
            "hands_count": hands_detected
        }
        
        print(f"✅ Response: {response}")
        return jsonify(response)

    except Exception as e:
        print(f"❌ General error: {e}")
        return jsonify({"error": f"Server error: {str(e)}", "success": False}), 500

def count_fingers(landmarks):
    """Simple finger counting based on landmarks"""
    try:
        # Finger tip positions (MediaPipe hand landmarks)
        tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        
        fingers_up = 0
        
        # Thumb (special case)
        if landmarks[4][0] > landmarks[3][0]:  # Tip further right than IP joint
            fingers_up += 1
            
        # Other fingers
        for tip_id in [8, 12, 16, 20]:  # Index, Middle, Ring, Pinky
            if landmarks[tip_id][1] < landmarks[tip_id-2][1]:  # Tip above MCP joint
                fingers_up += 1
        
        # Return gesture based on finger count
        if fingers_up == 0:
            return "✊ Fist"
        elif fingers_up == 1:
            return "☝️ One finger"
        elif fingers_up == 2:
            return "✌️ Two fingers"
        elif fingers_up == 3:
            return "🖖 Three fingers"
        elif fingers_up == 4:
            return "🖐️ Four fingers"
        elif fingers_up == 5:
            return "✋ Open hand"
        else:
            return f"🤚 {fingers_up} fingers"
            
    except Exception as e:
        return "👋 Hand detected"

# Serve HTML files specifically
@app.route("/hearing.html")
def serve_hearing():
    return send_from_directory(".", "hearing.html")

@app.route("/index.html")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/style.css")
def serve_css():
    return send_from_directory(".", "style.css")

if __name__ == "__main__":
    print("🚀 Starting fixed server...")
    print("📝 API endpoints:")
    print("   GET  / - Server status")
    print("   GET  /test - JSON test") 
    print("   POST /sign-to-text - Hand detection")
    print("📄 HTML files:")
    print("   /hearing.html - Main interface")
    app.run(host="0.0.0.0", port=5000, debug=True)
