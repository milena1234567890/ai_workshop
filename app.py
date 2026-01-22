from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
import os


load_dotenv()

SUPABASE_URL = os.environ.get("FIRST_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get ("FIRST_SUPABASE_SERVICE_ROLE_KEY")
sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# app = Flask(__name__, static_folder="public", static_url_path="")
# client = OpenAi(api_key = os.environ.get("OPEN_API_KEY"))

app = Flask(__name__)
client = OpenAI()

def build_system_prompt(user_message: str, rag_context: str) -> list[dict]:
    # Simple greetings get a very short, friendly response
    simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon"]
    if user_message.lower().strip() in simple_greetings:
        system_content = (
            "You are a friendly language-learning expert. "
            "Respond in short, neutral, and approachable sentences."
        )
    else:
        system_content = (
            "You are an expert linguist and language-learning coach. "
            "You ALWAYS give structured answers.\n\n"
            "Follow this exact structure when answering:\n"
            "1. Short overview (1–2 sentences)\n"
            "2. Step-by-step guidance (numbered list)\n"
            "3. Practical tips or examples (bullet points)\n"
            "4. Common mistakes to avoid\n"
            "5. Clear next steps\n\n"
            "Use headings, keep explanations clear and concise, "
            "and adapt advice to the specific language mentioned by the user."
        )

    # Add RAG context if available
    context_content = (
        "Use the retrieved context below only if it is directly relevant. "
        "If it doesn't help, ignore it.\n\n"
        f"RETRIEVED CONTEXT: {rag_context if rag_context else '(no matches)'}"
    )

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_message},
        {"role": "system", "content": context_content}
    ]



def chatbot_response(user_prompt):
    messages = build_system_prompt(user_prompt, rag_prompt)

    response = client.responses.create(
        model="gpt-5-nano",
        input=messages
    )
    return response.output_text

def chatbot_response(user_prompt, rag_prompt):
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "system",
                "content": (
                "You are an expert linguist and language-learning coach. "
                "When a user asks a question that requires a long answer, give structured answers following this format. Otherwise, answer as briefly as possible in 1-2 lines.\n" 
                "ONLY IF USER ASKS A LONG QUESTION:"
                "You are a calm, friendly, human-like chatbot. "
                "Respond in short, neutral sentences first. "
                "Use a short Title (2–6 words) and bullet points only if they add value. "
                "Only give detailed step-by-step guidance if the user explicitly asks for it. "
                "If the user input is unclear, ask one short open-ended question to clarify. "
                "Avoid filler words like 'Overview', 'Here’s how', or 'Let’s break this down'. "
                "Keep explanations simple and easy to understand. "
                "Adapt your advice to the language or topic the user mentions. "
                "Do not provide long templates unless requested."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            },
            {
                "role": "system",
                "content": rag_prompt
            }
        ]
    )
    return response.output_text

# takes in the string and outputs a vector
def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def semantic_search(query_text: str) -> list[dict]:
    emb_q = embed_query(query_text)
    res = sb.rpc("match_chunks", {"query_embedding": emb_q, "match_count" : 5}).execute()
    rows = res.data or []
    #for easier debugging
    print("RAG OUTPUT:", rows)
    return rows

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # conduct symentic search
    rag_rows = semantic_search(user_message)

    # fixes our formatting
    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    # # create the rag prompt 
    # rag_message = {
    #     "role": "system", 
    #     "content": (
    #         "Use the retrieve context below to answer. If it doesn't contain the answer, say so. \n\n"
    #         f"RETRIEVE CONTEXT: \n{context if context else '(no matches)' } "
    #     )
    # }
 


    reply = chatbot_response(user_message, context)
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

    