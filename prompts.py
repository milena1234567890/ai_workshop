

def build_system_prompt(user_message: str, rag_context: str) -> list[dict]:
    # Determine if the user input is simple or complex
    simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon"]
    if user_message.lower().strip() in simple_greetings:
        system_content = (
            "You are a friendly language-learning expert. "
            "Respond in a way a user can easily understand. "
            "Keep it short, engaging, and approachable."
        )
    else:
        system_content = (
            "You are an expert linguist and language-learning coach. "
            "When a user asks a question, ALWAYS give structured answers following this format:\n"
            "1. Short overview (1–2 sentences)\n"
            "2. Step-by-step guidance (numbered list)\n"
            "3. Practical tips or examples (bullet points)\n"
            "4. Common mistakes to avoid\n"
            "5. Clear next steps\n\n"
            "Use headings, keep explanations clear and concise, "
            "and adapt advice to the language mentioned by the user."
        )

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_message},
        {"role": "system", "content": (
            "Use the retrieved context below to answer the question. "
            "If the context doesn't contain the answer, respond based on your knowledge.\n\n"
            f"RETRIEVED CONTEXT: {rag_context if rag_context else '(no matches)'}"
        )}
    ]