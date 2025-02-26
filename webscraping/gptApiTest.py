import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI()
text = "hi"
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"""Please summarize the following text in 
        less than 100 words:\n\n{text}"""}
    ]
)

# Extract the text from the response correctly
text_output = completion.choices[0].message.content  # Access using dot notation

# Print just the text output
print(text_output)
