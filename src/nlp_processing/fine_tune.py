import pandas as pd
from transformers import GPTJForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
import logging

#Separate logger for fine-tuning
fine_tune_logger = logging.getLogger("fine_tune")
fine_tune_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('fine_tune.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
fine_tune_logger.addHandler(file_handler)

fine_tune_logger.info("Starting fine-tuning process")
excel_path = '../../data/chat_data/chat_data.xlsx'
df = pd.read_excel(excel_path)

fine_tune_logger.info(f"Loaded {len(df)} rows of data from Excel")
dataset = Dataset.from_pandas(df)
fine_tune_logger.info("Loading model and tokenizer")

model = GPTJForCausalLM.from_pretrained('../../models/base_model')
tokenizer = AutoTokenizer.from_pretrained('../../models/base_model')

def tokenize_function(examples):
    return tokenizer(examples['text'], padding="longest", truncation=True, max_length=1024)

tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset.save_to_disk('../../data/processed_data/tokenized_chat_data')
fine_tune_logger.info("Tokenization complete and saved to disk")

#Data collator for language modeling (for dynamic padding)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

#Set up Trainer
training_args = TrainingArguments(
    output_dir='../../models/trained_model',           #Directory for saving fine-tuned model
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=3,                                
    logging_dir='../../logs',                          #Directory for logging
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,                   #Use the entire dataset for training
    data_collator=data_collator,
)

fine_tune_logger.info("Starting model training")
trainer.train()

fine_tune_logger.info("Saving fine-tuned model and tokenizer")
model.save_pretrained('../../models/trained_model')
tokenizer.save_pretrained('../../models/trained_model')

fine_tune_logger.info("Fine-tuning complete. Model saved.")
print("Fine-tuning complete. Model saved to models/trained_model")
