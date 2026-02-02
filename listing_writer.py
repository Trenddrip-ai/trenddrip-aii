# listing_writer.py
from openai import OpenAI

client = OpenAI()

def create_listing(prompt_used):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert Etsy POD seller who writes high-converting listings for streetwear graphic t-shirts."
            },
            {
                "role": "user",
                "content": f"""
A t-shirt design was created with this concept:

{prompt_used}

Write:

1) A catchy Etsy title (max 140 characters)
2) 13 Etsy tags separated by commas
3) A persuasive product description

Make it optimized for search and streetwear buyers.
"""
            }
        ]
    )

    return response.choices[0].message.content
