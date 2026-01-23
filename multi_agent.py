# # from flask import Flask, request, jsonify, send_from_directory
# # from flask_cors import CORS
# # from openai import OpenAI
# # from dotenv import load_dotenv
# # from prompts import system_prompt1, system_prompt2
# # import os
# # from supabase import create_client
# # import spotipy
# # from spotipy.oauth2 import SpotifyClientCredentials

# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv
# from openai import OpenAI
# from supabase import create_client
# import os

# load_dotenv()

# FIRST_SUPABASE_URL = os.getenv("FIRST_SUPABASE_URL")
# FIRST_SUPABASE_KEY = os.getenv("FIRST_SUPABASE_SERVICE_ROLE_KEY")
# supabase1 = create_client(FIRST_SUPABASE_URL, FIRST_SUPABASE_KEY)

# SECOND_SUPABASE_URL = os.getenv("SECOND_SUPABASE_URL")
# SECOND_SUPABASE_KEY = os.getenv("SECOND_SUPABASE_SERVICE_ROLE_KEY")
# supabase2 = create_client(SECOND_SUPABASE_URL, SECOND_SUPABASE_KEY)

# client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

# # sheet_content = "\n".join([
# #     f"{doc.get('topic', doc.get('title', 'No Title'))}: {doc.get('content', 'No Content')}"
# #     for doc in documents
# # ])
                
# # takes in the string and outputs a vector
# def embed_query(text: str) -> list[float]:
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )

#     return response.data[0].embedding

# # takes as input a query, conducts the search, returns context
# def semantic_search(query_text, sb_client) -> list[dict]:
#     emb_q = embed_query(query_text)
#     res = sb_client.rpc(
#         "match_chunks",
#         {"query_embedding": emb_q, "match_count": 5}
#     ).execute()
#     return res.data or []

# def run_bot(user_message, system_prompt, sb_client) -> str:
#     rag_rows = semantic_search(user_message, sb_client)

#     # fixes our formatting
#     context = "\n\n".join(
#         f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
#         for i, row in enumerate(rag_rows)
#     )

#     # create the rag prompt
#     rag_message = {
#         "role": "system",
#         "content": (
#             "Use the retrieved context below to answer. If it doesn't contain the answer, say so. \n\n"
#             f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
#         ) }

#     full_user_message = {
#         "role": "user",
#         "content": user_message
#     }

#     system_prompt1 = {
#     "role": "system",
#     "content": (
#         "You are an expert linguist and language-learning coach. "
#         "When a user asks a question, ALWAYS give structured answers following this format:\n"
#         "1. Short overview (1–2 sentences)\n"
#         "2. Step-by-step guidance (numbered list)\n"
#         "3. Practical tips or examples (bullet points)\n"
#         "4. Common mistakes to avoid\n"
#         "5. Clear next steps\n\n"
#         "Use headings, keep explanations clear and concise, "
#         "and adapt advice to the language mentioned by the user.\n\n"
#         "Use the retrieved context below to answer the question. "
#         "If the context doesn't contain the answer, respond based on your knowledge.\n\n"
#         "RETRIEVED CONTEXT:\n(no matches)"
#     )
     
# }
#     full_message = [rag_message, full_user_message, system_prompt]

#     resp = client.responses.create(
#         model = "gpt-5-nano",
#         input=full_message
#     )

#     return resp.output_text

# def chatbotone(user_message):
#     return run_bot(user_message, system_prompt1, supabase1)

# def chatbotwo(user_message):
#     return run_bot(user_message, system_prompt2, supabase2)

# def simulation():
#     #contain the output at any given time
#     output = chatbotone("Ask a question about something that interests you.")
#     print("Chatbotone says:" + output)

#     for _ in range(5):
#         output = chatbotwo(output)
#         print("Chatbotwo says:" + output)

#         output = chatbotone(output)
#         print("Chatbotone says:" + output)

# simulation()

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client
import os

load_dotenv()

FIRST_SUPABASE_URL = os.getenv("FIRST_SUPABASE_URL")
FIRST_SUPABASE_KEY = os.getenv("FIRST_SUPABASE_SERVICE_ROLE_KEY")
supabase1 = create_client(FIRST_SUPABASE_URL, FIRST_SUPABASE_KEY)

SECOND_SUPABASE_URL = os.getenv("SECOND_SUPABASE_URL")
SECOND_SUPABASE_KEY = os.getenv("SECOND_SUPABASE_SERVICE_ROLE_KEY")
supabase2 = create_client(SECOND_SUPABASE_URL, SECOND_SUPABASE_KEY)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -------------------------
# GLOBAL SYSTEM PROMPTS
# -------------------------

system_prompt1 = {
    "role": "system",
    "content": (
        "You are an expert linguist and language-learning coach. "
        "But  when you start your conversation don't mention in which field you are an expert in. IT IS VERY IMPORTANT NOT to mention the profession in the beginning and then once the partner realizes through the conversation what you are doing for living - only then you can begin mentioning what you are doing and advice in your field"
        "In the beginning keep it maximum 300 words reply, but even shorter. It should be like a human conversation:"
                "When your partner asks a question:"  
        
        "Give structured answers following this format, only once the conversation friend has guessed what you are expert in:\n"
        "1. Short overview (1–2 sentences) about what you're doing. You can also say something like -- You guessed it correctly - I'm the expert in... \n"
        "2. Step-by-step guidance (numbered list), only if the conversation partner asks questions about learning a language\n"
        "3. Practical tips or examples (bullet points). Give these once you receive a question about learning a language\n"
        "4. Common mistakes to avoid ( if needed in the particular question) \n"
        "5. Clear next steps ( Very important ) \n\n"
        "Use headings(make them clearly bigger), keep explanations clear and concise (don't overexplain things, keep it short and simple to the human being), "
        "and adapt advice to the language mentioned by the user."
    )
}

# THIS IS VERY FRIST PROMPT, WE DID NOT CHANGE HERE ANYTHING


# system_prompt1 = {
#     "role": "system",
#     "content": (
#         "You are an expert linguist and language-learning coach. "
#         "When a user asks a question, ALWAYS give structured answers following this format:\n"
#         "1. Short overview (1–2 sentences)\n"
#         "2. Step-by-step guidance (numbered list)\n"
#         "3. Practical tips or examples (bullet points)\n"
#         "4. Common mistakes to avoid\n"
#         "5. Clear next steps\n\n"
#         "Use headings, keep explanations clear and concise, "
#         "and adapt advice to the language mentioned by the user."
#     )
# }

system_prompt2 = {
    "role": "system",
    "content": (
        "You are an expert in music. You know almost every song in the world and now you can do the following: find music fron the context, tell the script of the chosen song"
        "from the context tell which song is that "
        "Create a new song based on the knowledge you have"
        "Tell the story of the creators and actors"
        "Inform about the upcoming concerts to keep the trends as well"
        "You are chatbot 2, a helpful and observant assistant. You are about to have a conversation with friend, who has a specific goal and profession that you must find out. For now you don't know it, you have to figure it out on your own."
        "Important rules: At the start, you do not know  friend’s goal and profession"
        "Your task is to ask questions, observe hints, and respond naturally to figure out what friend is doing for living."
        "Once you infer friend’s goal, you can start giving more focused advice or solutions, but never assume it too early."
        "Stay polite, curious, and adaptive in your responses."
        "Begin the conversation with a friendly greeting and some open-ended questions to understand your friend’s intentions."
        "Conversation rules:"
        "In your first message only, greet Agent B and ask a polite opener (e.g., “Hi, how are you?” or similar)."
        "In all later messages,"
        "Do NOT greet again"
        "Do NOT ask “how are you?” again"
        "Do NOT repeat introductions or pleasantries"
        "Continue the conversation naturally and directly based on the topic and prior context."
        "Stay consistent with the conversation flow and avoid restarting the interaction."
        "Goal behavior:"
        "Be natural and cooperative."
        "Focus on progressing the discussion instead of re-opening it."
        "Treat the conversation as ongoing after the first turn."
            )
}

# -------------------------
# EMBEDDING + SEARCH
# -------------------------

def embed_query(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def semantic_search(query_text, sb_client) -> list[dict]:
    emb_q = embed_query(query_text)
    res = sb_client.rpc(
        "match_chunks",
        {"query_embedding": emb_q, "match_count": 5}
    ).execute()
    return res.data or []

# -------------------------
# CORE BOT LOGIC
# -------------------------

def run_bot(user_message, system_prompt, sb_client) -> str:
    rag_rows = semantic_search(user_message, sb_client)

    context = "\n\n".join(
        f"[Source {i+1} | sim={row.get('similarity'):.3f}]\n{row.get('content','')}"
        for i, row in enumerate(rag_rows)
    )

    rag_message = {
        "role": "system",
        "content": (
            "Use the retrieved context below to answer the question. "
            "If the context doesn't contain the answer, respond based on your knowledge.\n\n"
            f"RETRIEVED CONTEXT:\n{context if context else '(no matches)'}"
        )
    }

    full_user_message = {
        "role": "user",
        "content": user_message
    }

    # ✅ Correct order: system → user → rag
    full_message = [
        system_prompt,
        full_user_message,
        rag_message
    ]

    resp = client.responses.create(
        model="gpt-5-nano",
        input=full_message
    )

    return resp.output_text

# -------------------------
# BOT WRAPPERS
# -------------------------

def chatbotone(user_message):
    return run_bot(user_message, system_prompt1, supabase2)

def chatbotwo(user_message):
    return run_bot(user_message, system_prompt2, supabase1)

# -------------------------
# SIMULATION
# -------------------------

def print_block(title: str, content: str):
    line = "-" * 75
    print("\n" + line)
    print(f"{title.center(75)}")
    print(line)
    print("\n" + content + "\n")
    print(line + "\n")


def simulation():
    output = chatbotone("Ask a question about something that interests you.")

    print_block(
        "SIMULATION — CHATBOT ONE",
        output
    )

    for i in range(5):
        output = chatbotwo(output)

        print_block(
            f"SIMULATION — CHATBOT TWO (ROUND {i + 1})",
            output
        )

        output = chatbotone(output)

        print_block(
            f"SIMULATION — CHATBOT ONE (ROUND {i + 1})",
            output
        )


if __name__ == "__main__":
    simulation()