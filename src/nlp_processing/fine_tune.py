import torch
from transformers import GPTNeoForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

# Load the model and tokenizer from your local directory
model = GPTNeoForCausalLM.from_pretrained('../../models/base_model')
tokenizer = AutoTokenizer.from_pretrained('../../models/base_model')

# Load your processed chat data (assumed to be in a dataset format, update the path accordingly)
dataset = load_dataset('json', data_files='../../data/processed_data/chat_dataset.json')

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Data collator for language modeling (for dynamic padding)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Set up Trainer
training_args = TrainingArguments(
    output_dir='../../models/trained_model',           # Directory for saving fine-tuned model
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,                                # Adjust as needed
    logging_dir='../../logs',                          # Directory for logging
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],          # Assuming your dataset has a train split
    eval_dataset=tokenized_dataset['validation'],      # Assuming your dataset has a validation split
    data_collator=data_collator,
)

# Start training
trainer.train()

# Save the fine-tuned model
model.save_pretrained('../../models/trained_model')
tokenizer.save_pretrained('../../models/trained_model')

print("Fine-tuning complete. Model saved to models/trained_model")
