from fastapi import FastAPI, File, UploadFile
import requests
import base64

app = FastAPI()

# Put your Gemini API key here or set it in environment variable
API_KEY = "AIzaSyDeUE_ZVwNOi4UGznyH6j1jfMYBNkO8hKs"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

@app.get("/")
def root():
    return {"message": "Welcome to Gemini Funny Image Dialogue API"}

@app.post("/funny-dialogues")
async def funny_dialogues(file: UploadFile = File(...)):
    """
    Upload an image and get funny dialogues related to it.
    """

    # Read file and encode as base64
    file_bytes = await file.read()
    image_base64 = base64.b64encode(file_bytes).decode("utf-8")

    # Prompt for Gemini
    prompt = """
Act like a Telugu comedy lyricist + Instagram meme creator.
Generate super short and funny parody-style lines in English letters (Telugu transliteration).

⚡ Rules:

Meaning should be Telugu but words in English alphabets.

Lines must feel like parody song bits or Instagram meme punchlines.

Keep it under 1–2 lines (short & catchy).

Make them hilarious, youthful, and relatable (food, exams, love, WiFi, parents, etc).

Give me 15 different lines.

🎵 Example style (don’t copy, create new):

'Love pain ante… data pack ayipoyina feeling la undi!'

'Class lo nenu silent… but canteen lo violent!'
"""



    # Call Gemini API
    response = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": file.content_type,
                                "data": image_base64,
                            }
                        },
                    ]
                }
            ]
        },
    )

    data = response.json()

    # Extract generated dialogues safely
    try:
        dialogues = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        dialogues = f"Sorry, could not generate funny dialogues. Response: {data}"

    return {
        "filename": file.filename,
        "funny_dialogues": dialogues
    }

