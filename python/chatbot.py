from gpt4all import GPT4All

model_path = "models/llama3-8b-instruct.Q4_0.gguf"
model = GPT4All(model_path)

def chat_with_ai(prompt):
    response = model.chat(prompt)
    return response

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chat_with_ai(user_input)
    print("Bot:", response)
