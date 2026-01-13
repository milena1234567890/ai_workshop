from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

app = Flask(__name__)

def chatbot_response(user_prompt):
    response = client.responses.create(
        model="gpt-5-nano",
        input=user_prompt
    )
    return response.output_text

# def chatbot_response(user_prompt):
#     response = client.responses.create(
#         model="gpt-5-nano",
#         input=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an expert linguist and language-learning coach. "
#                     "You ALWAYS give structured answers.\n\n"
#                     "Follow this exact structure when answering:\n"
#                     "1. Short overview (1–2 sentences)\n"
#                     "2. Step-by-step guidance (numbered list)\n"
#                     "3. Practical tips or examples (bullet points)\n"
#                     "4. Common mistakes to avoid\n"
#                     "5. Clear next steps\n\n"
#                     "Use headings, keep explanations clear and concise, "
#                     "and adapt advice to the specific language mentioned by the user."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": user_prompt
#             }
#         ]
#     )
#     return response.output_text



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = chatbot_response(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
