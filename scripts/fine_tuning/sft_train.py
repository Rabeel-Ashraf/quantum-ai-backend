#!/usr/bin/env python3
"""
Supervised Fine-Tuning script for domain-specific improvements
"""

import torch
from transformers import TrainingArguments, Trainer
from datasets import Dataset
import json
from pathlib import Path

def load_training_data(data_path):
    """Load training data from JSON file"""
    with open(data_path, 'r') as f:
        data = json.load(f)
    return Dataset.from_list(data)

def train_sft_model(model, tokenizer, train_data, output_dir):
    """Train model using supervised fine-tuning"""
    
    # Tokenize the data
    def tokenize_function(examples):
        return tokenizer(
            examples["text"], 
            padding="max_length", 
            truncation=True, 
            max_length=512
        )
    
    tokenized_data = train_data.map(tokenize_function, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="no",
        save_strategy="epoch",
        load_best_model_at_end=False,
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data,
        tokenizer=tokenizer,
    )
    
    # Train the model
    trainer.train()
    
    # Save the model
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    print("SFT training script - import this module to use")
