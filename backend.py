from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure API key
genai.configure(api_key="AIzaSyB67TXK0zGnV39fIEg0FBm9s1a2qEFZxbU")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

@app.route('/')
def index():
    return open('frontend.html').read()

@app.route('/bug_report', methods=['POST'])
def generate_bug_report():
    # Get code from the frontend
    code = request.json.get('code')

    # Start a conversation with the model
    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": [f"You are an expert software developer reviewing code submissions. Your task is to debug the code provided by the user and provide a corrected version along with an explanation of the issue.\n\nCode provided by the user:\n{code}\n\nExplanation of the issue and corrected code:\n\n1. Issue: [DESCRIBE_ISSUE_HERE]\n   Corrected code:\n   [CORRECTED_CODE_HERE]\n\n2. Issue: [DESCRIBE_ISSUE_HERE]\n   Corrected code:\n   [CORRECTED_CODE_HERE]\n\n[ADDITIONAL_ISSUES_AND_CORRECTIONS_IF_ANY]\nReplace [USER_CODE] with the actual code provided by the user. In the explanation section, describe each issue found in the code along with the corrected version. If there are multiple issues, you can list them sequentially with their corresponding corrected code."]
        },
        {
            "role": "model",
            "parts": ["Okay, I'm ready to analyze and debug the code. Please provide the [USER_CODE] you want me to review. Remember, the more context you give about the purpose of the code and the issues you're facing, the better I can assist you."]
        },
    ])

    convo.send_message(code)
    response = convo.last.text

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
