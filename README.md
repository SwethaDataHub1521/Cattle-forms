## 🧠 Project Overview  

This project integrates **Computer Vision**, **Generative AI**, and **Cloud-based Analytics** to assess cattle health.  
It contains two intelligent modules:

1. **Cattle Behavior Analysis (Flask + Gemini API)** – analyzes cow posture, eyes, and mouth using computer-vision techniques and provides an AI-generated health report through Google Gemini.  
2. **Cattle Disease Prediction (Streamlit + g4f)** – predicts likely diseases based on facial-expression descriptions using GPT-style reasoning.

The goal is to enable **early detection of cattle health issues** and support smart-farming systems.

---

## ⚙️ Features  

### 🧩 Behavior Analysis (Flask + Gemini)
- 📸 Upload cow images for AI-driven behavior insights  
- 🧠 Uses **OpenCV** to extract posture, eye, and mouth features  
- ☁️ Sends metrics to **Gemini Pro API** for interpretation  
- 🩺 Returns detailed, natural-language health analysis  

### 💬 Disease Prediction (Streamlit + g4f)
- ✍️ Accepts text-based facial-expression descriptions  
- 🐮 Uses **g4f (GPT-4o-mini)** to infer probable diseases  
- 📊 Produces confidence levels and practical recommendations  

---

## 🧰 Technologies Used  

| Component | Technology |
|------------|-------------|
| Language | Python 3.x |
| Frameworks | Flask, Streamlit |
| AI / LLMs | Google Gemini API, g4f (GPT-4o-mini) |
| Image Processing | OpenCV, NumPy |
| Libraries | Pillow, Werkzeug, requests |

---

## 📦 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/cattle-ai-analysis.git
cd cattle-ai-analysis
2️⃣ Create Virtual Environment (optional)
bash
Copy code
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
3️⃣ Install Dependencies
bash
Copy code
pip install flask opencv-python numpy pillow google-generativeai streamlit g4f
🧠 How It Works
🧩 Flask Module – Cattle Behavior Analysis
Upload a cattle image via upload.html.

System extracts: posture angle, eye brightness, mouth status, color dominance.

Sends metrics to Gemini API.

Displays AI-generated behavior and health analysis.

Run:

bash
Copy code
python app.py
Open → http://127.0.0.1:5000

💬 Streamlit Module – Disease Prediction
Upload an optional cattle image.

Describe facial expressions (e.g., droopy eyes, lowered head).

g4f GPT-4o-mini analyzes text and predicts diseases.

Run:

bash
Copy code
streamlit run disease_predictor.py
📁 Project Structure
bash
Copy code
cattle-ai-analysis/
│
├── app.py                 # Flask + Gemini backend  
├── templates/
│   └── upload.html        # Upload UI  
├── uploads/               # Uploaded images  
├── disease_predictor.py   # Streamlit + g4f frontend  
├── requirements.txt       # Dependencies  
└── README.md              # Documentation  
🧪 Example Outputs
Flask (Gemini Analysis)
yaml
Copy code
Posture Angle: 14.5°
Eye Visibility: Visible
Mouth Status: Possibly open
AI Assessment:
The cow shows mild fatigue but normal alertness.  
Recommend observation for 24 hours and adequate hydration.
Streamlit (g4f Prediction)
yaml
Copy code
Predicted Disease: Bovine Respiratory Disease (BRD)
Expression Cues: Droopy eyes, open mouth, lowered head
Confidence: High
Recommendation: Immediate veterinary check-up.
🔮 Future Enhancements
🎥 Add real-time video feed analysis

📱 Build mobile app dashboard for farmers

🧠 Train CNN models for direct image disease detection

☁️ Integrate Firebase for data storage and notifications

👩‍💻 Author
Swetha S
MCA – Data Analyst
💡 Passionate about AI, Cloud Computing & Smart Agriculture Solutions

📜 License
This project is open-source and available under the MIT License.
You are free to use and modify it for academic or research purposes.
