import streamlit as st
from g4f.client import Client
from PIL import Image

# Configure Streamlit page
st.set_page_config(page_title="Cattle Disease Prediction (g4f)", page_icon="🐄")
st.title("Cattle Disease Prediction Based on Facial Expressions (g4f)")
st.markdown(
    "Upload a cattle image and describe its facial expressions. The g4f library (using gpt-4o-mini) will predict potential diseases based on the description."
)
st.warning("Note: g4f does not support direct image analysis. Please provide a detailed text description of the cattle's facial expressions.")

# Initialize g4f client
try:
    client = Client()
except Exception as e:
    st.error(f"Error initializing g4f client: {e}")
    st.stop()

# Image upload
uploaded_file = st.file_uploader("Upload a cattle image (JPEG/PNG, for reference)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Cattle Image", use_column_width=True)

# Text input for facial expression description
expression_description = st.text_area(
    "Describe the cattle's facial expressions",
    placeholder="e.g., droopy eyes, tense mouth, lowered head, drooping ears",
    help="Provide details about eye appearance, ear position, mouth/jaw, and head position."
)

if expression_description:
    # Define the prompt
    prompt = f"""
    You are a veterinary AI assistant with expertise in cattle health. Based on the following description of a cattle's facial expressions, predict potential diseases. The description is: "{expression_description}"

    Focus on facial expression cues, such as:
    - Eye appearance (e.g., droopy, sunken, squinted, or watery eyes indicating lethargy, pain, or stress).
    - Ear position (e.g., drooping, pinned back, or asymmetrical ears suggesting discomfort or illness).
    - Mouth and jaw (e.g., tensed mouth, open mouth, or excessive salivation indicating pain or distress).
    - Head position (e.g., lowered head, tilted head, or rigid posture signaling weakness or neurological issues).

    Predict possible diseases, such as bovine respiratory disease (BRD), mastitis, ketosis, lameness, foot-and-mouth disease, or other relevant conditions. For each prediction, provide:
    - The predicted disease name.
    - A list of specific expression cues from the description.
    - A confidence level (high, medium, low).
    - An explanation of how the expressions correlate with the disease, referencing veterinary knowledge.

    If the expressions appear normal or no clear disease-related cues are described, state that the cattle appears healthy and recommend further clinical examination. If the description is vague, note the limitation and suggest a more detailed input.

    Format your response as follows:
    - **Predicted Disease**: [Disease Name]
      - **Expression Cues**: [List of observed cues]
      - **Confidence**: [High/Medium/Low]
      - **Explanation**: [How the expressions suggest this disease]
    - **Overall Assessment**: [Summary of findings]
    - **Recommendations**: [Next steps]
    - **Limitations**: [Any issues with the description]
    """

    # Button to trigger analysis
    if st.button("Analyze Expressions"):
        with st.spinner("Analyzing cattle expressions with g4f..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    web_search=False
                )
                st.subheader("Cattle Disease Prediction Results")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error with g4f request: {e}")
                st.markdown(
                    "Possible issues: Model 'gpt-4o-mini' unavailable or rate-limited. "
                    "Try again or use another model (e.g., 'gpt-3.5-turbo')."
                )
else:
    st.info("Please upload an image and describe the cattle's facial expressions to begin analysis.")