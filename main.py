import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
import google.generativeai as genai  # ✅ USING GEMINI

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Configure Gemini API KEY (use environment variable or hardcode for testing)
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyCNnlYg3zs4AXLCsg6cQMKshhnTKXPlTfw")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_visual_features(image_path):
    """Extract basic visual features from cow image"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
            
        # Basic image processing
        img = cv2.resize(img, (224, 224))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Simple feature extraction (replace with proper CV in production)
        edges = cv2.Canny(gray, 100, 200)
        edge_intensity = np.mean(edges)
        
        # Color analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_dominance = np.mean(hsv[:,:,0])  # Hue channel
        
        return {
            'posture_angle': estimate_posture_angle(img),
            'eye_brightness': analyze_eyes(gray),
            'mouth_openness': analyze_mouth(gray),
            'edge_intensity': edge_intensity,
            'color_dominance': color_dominance
        }
    except Exception as e:
        print(f"Feature extraction error: {e}")
        return None

def estimate_posture_angle(img):
    """Very simplified posture estimation"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
    
    if lines is not None:
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angles.append(angle)
        return np.median(angles) if angles else 0
    return 0

def analyze_eyes(gray_img):
    """Simplified eye analysis"""
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray_img, 1.1, 4)
    return len(eyes) > 0  # Just checking visibility

def analyze_mouth(gray_img):
    """Simplified mouth analysis"""
    lower_face = gray_img[gray_img.shape[0]//2:, :]
    return np.mean(lower_face) < 100  # Dark area might indicate open mouth

def generate_behavior_analysis(features):
    """Generate detailed behavior analysis using Gemini API"""
    try:
        prompt = f"""Analyze this cow's health based on the following behavioral metrics:
        
        Posture Angle: {features['posture_angle']} degrees
        Eye Visibility: {'Visible' if features['eye_brightness'] else 'Not clearly visible'}
        Mouth Status: {'Possibly open' if features['mouth_openness'] else 'Possibly closed'}
        Edge Intensity: {features['edge_intensity']:.2f}
        Color Dominance: {features['color_dominance']:.2f} (HSV Hue)
        
        Consider these aspects:
        1. Behavioral Patterns: Resting, grazing, or unusual movements
        2. Posture Analysis: Normal stance or signs of discomfort
        3. Feeding Habits: Signs of normal or abnormal eating
        4. Facial Expressions: Indicators of stress or pain
        5. Coat Condition: Health indicators from fur appearance
        
        Provide a detailed health assessment with recommendations."""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print(f"AI analysis error: {e}")
        return "Behavioral analysis unavailable (API error)"

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/analyze', methods=['POST'])
def analyze_behavior():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            features = extract_visual_features(filepath)
            if features is None:
                return jsonify({"error": "Feature extraction failed"}), 500
            
            analysis = generate_behavior_analysis(features)
            
            return jsonify({
                "status": "success",
                "analysis": analysis,
                "features": features
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
