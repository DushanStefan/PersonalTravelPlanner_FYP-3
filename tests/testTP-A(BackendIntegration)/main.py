from agents.tool_agent.prompts import zeroshot_react_agent_prompt
from agents.tool_agent.tool_agent import ReactAgent
from chat.chat_manager import handle_chat
from flask_cors import CORS  # Import CORS

from flask import Flask, jsonify, request
import json

app = Flask(__name__)
CORS(app)

def main():
    chat_history_path = "chat_history.txt"
    return chat_history_path

@app.route("/click", methods=["POST"])
def handle():
    chat_history_path = main()
    message = request.json.get("message")
    bot_reply = handle_chat(chat_history_path,message)
    return jsonify({"reply": bot_reply})
    
    



# TODO: improve the NLP classifier
if __name__ == "__main__":
    app.run(debug=False)
    