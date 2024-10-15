from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from src.error_handling.exceptions import NLPProcessingError

# Load GPT-Neo model and tokenizer (loaded once at the top)
model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(input_text):
    """Generate a text response from the model based on input."""
    try:
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=150)
        return tokenizer.decode(outputs[0], skip_special_tokens=True) if outputs else ""
    except Exception as e:
        raise NLPProcessingError(f"Error generating response: {str(e)}")

def extract_urls(input_text):
    """Extract URLs from the input text using regex."""
    url_pattern = r"(https?://\S+)"
    return re.findall(url_pattern, input_text)

def detect_intent(generated_text):
    """Detect intent from generated text by looking for structured intent patterns."""
    try:
        if "intent:" in generated_text:
            return generated_text.split("intent:")[1].split()[0].strip()
        else:
            return "unknown_intent"
    except Exception as e:
        raise NLPProcessingError(f"Error detecting intent: {str(e)}")

def process_with_gpt_j(input_text):
    """Main function to process input text, generate response, extract URLs, and detect intent."""
    try:
        # Generate a response from the model
        generated_text = generate_response(input_text)

        # Extract URLs from input
        urls = extract_urls(input_text)

        # Detect intent from generated text
        intent = detect_intent(generated_text)

        return {"intent": intent, "urls": urls}
    except Exception as e:
        raise NLPProcessingError(f"Error processing text: {str(e)}")
