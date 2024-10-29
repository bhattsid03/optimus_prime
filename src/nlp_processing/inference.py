import torch
from transformers import AutoTokenizer, GPTJForCausalLM
import re
from src.error_handling.exceptions import NLPProcessingError

# Load GPT-J model and tokenizer (loaded once at the top)
model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = GPTJForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to("mps")

# Static few-shot examples (will be tokenized and used once)
few_shot_prompt = """"
        "Here are a few examples of user requests and their intents:\n\n"
        "Input: 'The build failed at Jenkins job xyz. What went wrong?'\n"
        "Intent: 'Build Failure'\n\n"
        "Input: 'What is the status of https://gerrit.eng.nutanix.com/c/main/+/940392?'\n"
        "Intent: 'CR Status'\n\n"
        "Input: 'Please help with this failure. https://jenkins.example.com/job/12345'\n"
        "Intent: 'Build Failure'\n\n"
        "Input: 'the build is failing for this change. Can you please help here? https://gerrit.eng.nutanix.com/c/main/+/940392'\n"
        "Intent: 'Build Failure'\n\n"
        "Input: 'Jenkins pipeline failed: https://phx-p10y-jenkins-harbinger-prod-12.p10y.eng.nutanix.com/job/Precommit_NOS/job/infra-master/7498/ can you please help on it?'\n"
        "Intent: 'Build Failure'\n\n"
"""

# Generate reusable context once at the start (bot initialization)
def generate_context():
    inputs = tokenizer(few_shot_prompt, return_tensors="pt", padding=True, truncation=True).to("mps")
    return inputs.input_ids

# Global variable to hold the context
context = generate_context()  # Generated once

thread_memory = {}

def classify_intent(prompt, thread_id):
    """Classify intent from the prompt using the pre-generated context."""
    # Get thread-specific context (each thread stores its own inputs)
    if thread_id not in thread_memory:
        thread_memory[thread_id] = []

    # Append new input to the thread's memory
    thread_memory[thread_id].append(f'\nInput: "{prompt}"\nIntent:')

    # Combine the static context with the thread-specific memory
    full_prompt = tokenizer.decode(context[0], skip_special_tokens=True) + ''.join(thread_memory[thread_id])
    inputs = tokenizer(full_prompt, return_tensors="pt", padding=True, truncation=True).to("mps")

    # Generate response (predict intent)
    outputs = model.generate(inputs.input_ids, max_length=50, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract intent
    intent = generated_text.split("Intent:")[-1].split('\n')[0].strip()
    
    return intent

def extract_urls(input_text):
    """Extract URLs from the input text using regex."""
    url_pattern = r"(https?://\S+)"
    return re.findall(url_pattern, input_text)

def detect_intent(prompt, thread_id):
    """Detect intent by classifying it using the few-shot method."""
    try:
        intent = classify_intent(prompt, thread_id)
        return intent if intent else "unknown_intent"
    except Exception as e:
        raise NLPProcessingError(f"Error detecting intent: {str(e)}")

def process_with_gpt_j(input_text, thread_id):
    """Main function to process input text, extract URLs, and detect intent."""
    try:
        # Extract URLs from input
        urls = extract_urls(input_text)

        # Detect intent from generated text
        intent = detect_intent(input_text, thread_id)

        return {"intent": intent, "urls": urls}
    except Exception as e:
        raise NLPProcessingError(f"Error processing text: {str(e)}")
