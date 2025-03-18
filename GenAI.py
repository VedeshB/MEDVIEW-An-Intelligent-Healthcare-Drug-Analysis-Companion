from groq import Groq
def genai(initial):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content": initial,
                }
                ],
        model="llama3-8b-8192",
            )
    response=chat_completion.choices[0].message.content
    return response