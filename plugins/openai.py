import os
import pyrogram
from pyrogram import Client, filters
import openai
import re

OPENAI_API_KEY = os.environ.get('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')
openai.api_key = OPENAI_API_KEY

# Authentication code filter
def is_authenticated(message):
  return message.from_user.is_authenticated

# OpenAI command handler
@Client.on_message(filters.command("openai") and is_authenticated)
async def openai_command(client, message):
  text = message.text.split(" ")[1:]

  # Try to generate a completion from OpenAI
  try:
    response = openai.Completion.create(
      engine="davinci",
      prompt=text,
      max_tokens=1024,
      temperature=0.7,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
    )
  except Exception as e:
    # If an error occurs, send a message to the user
    await client.send_message(message.chat.id, f"Error: {e}")
  else:
    # If the completion was successful, send the completion to the user
    if response:
      await client.send_message(message.chat.id, response.choices[0].text)
    else:
      await client.send_message(message.chat.id, "OpenAI failed to generate a completion.")

# Connect command handler
def connect(payload):
  # Check if the authentication code is valid
  if payload["id"] != "chatcmpl-abc123":
    raise Exception("Invalid authentication code")

  # Send the response back to the user
  return {
    "id": "chatcmpl-abc123",
    "object": "chat.completion",
    "created": 1677858242,
    "model": "gpt-3.5-turbo-0613",
    "usage": {
      "prompt_tokens": 13,
      "completion_tokens": 7,
      "total_tokens": 20
    },
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "\n\nThis is a test!"
        },
        "finish_reason": "stop",
        "index": 0
      }
    ]
  }

# Start the client
Client.start()

# Listen for authentication codes
while True:
  payload = client.receive_message()
  if payload["type"] == "authenticationCode":
    connect(payload)
