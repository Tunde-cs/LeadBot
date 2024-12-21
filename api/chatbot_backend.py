import openai  # OpenAI for GPT-based responses
import os  # For environment variables (e.g., OpenAI API key)
from flask import Flask, request, jsonify, render_template  # Flask components
import logging  # For debugging purposes
from dotenv import load_dotenv
from flask_cors import CORS


# Load environment variables from .env
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://lead-bot.vercel.app"])

# Set up logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.route("/api/chat", methods=["GET", "POST"])  # Allow GET for debugging, POST for actual use
def chat():
    try:
        if request.method == "GET":
            # Provide a simple response for GET requests for quick health checks
            logging.info("GET request received on /chat endpoint.")
            return jsonify({"message": "Chat endpoint is running. Use POST to send messages."})

        # Retrieve user message from POST request
        user_message = request.json.get("message", "").strip()  # Strip leading/trailing spaces
        if not user_message:
            logging.warning("No user message provided in the request.")
            return jsonify({"error": "Message is required"}), 400

        logging.info(f"User message received: {user_message}")

        # System prompt for GPT-3.5 Turbo
        system_prompt = "You are a helpful assistant for a window replacement business. Provide concise and professional answers to help users with their queries about window options, costs, and installation."

        # Make API call to GPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract and log the chatbot's response
        answer = response['choices'][0]['message']['content']
        logging.info(f"Chatbot response: {answer}")

        # Return the chatbot's response
        return jsonify({"reply": answer})

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
        return jsonify({"error": "OpenAI API error occurred. Please try again later."}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
    
    # Vercel handler for serverless function
def handler(request, response):
    return app(request, response)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)  # Keep debug mode for development; turn it off in production


