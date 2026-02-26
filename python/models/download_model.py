from gpt4all import GPT4All

# Define the model name
model_name = "gpt4all-falcon-q4_0"

# Force a fresh download
GPT4All(model_name, allow_download=True)

print(f"Model '{model_name}' has been downloaded successfully!")