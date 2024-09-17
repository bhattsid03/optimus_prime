from transformers import GPTNeoForCausalLM, AutoTokenizer

# Load pre-trained GPT-Neo model and tokenizer
model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')  # Replace with larger models if needed
tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-neo-125M')

# Save the model and tokenizer to the project's base_model folder
model.save_pretrained('../../models/base_model')
tokenizer.save_pretrained('../../models/base_model')

print("GPT-Neo model and tokenizer saved to models/base_model")
