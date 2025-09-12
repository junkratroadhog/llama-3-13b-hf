import argparse
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model
import torch
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_model', type=str, required=True, help='Path to the base LLaMA model')
    parser.add_argument('--data', type=str, required=True, help='Path to logged_prompts.json')
    parser.add_argument('--output', type=str, default='./lora_weights', help='Output path for LoRA weights')
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--epochs', type=int, default=3)
    parser.add_argument('--fp16', action='store_true')
    parser.add_argument('--last_count_file', type=str, default='./last_trained_count.txt', help='File to track last trained prompt index')
    args = parser.parse_args()

    # Load tokenizer and base model
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        device_map='auto',
        load_in_4bit=True,
        torch_dtype=torch.float16
    )

    # Load logged prompts
    with open(args.data, 'r') as f:
        data_json = json.load(f)

    all_prompts = data_json['train']
    total_prompts = len(all_prompts)

    # Determine start index for incremental training
    last_count_file = Path(args.last_count_file)
    start_idx = 0
    if last_count_file.exists():
        start_idx = int(last_count_file.read_text())

    new_prompts = all_prompts[start_idx:]
    if len(new_prompts) == 0:
        print("No new prompts to train on.")
        return

    print(f"Training on {len(new_prompts)} new prompts (from index {start_idx})")

    # Prepare dataset
    dataset = Dataset.from_list(new_prompts)

    def tokenize(example):
        return tokenizer(example['prompt'], truncation=True, padding='max_length', max_length=512)

    tokenized_dataset = dataset.map(tokenize, batched=True)
    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    # LoRA config
    peft_config = LoraConfig(
        task_type="CAUSAL_LM",
        inference_mode=False,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1
    )
    model = get_peft_model(model, peft_config)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        save_strategy='epoch',
        logging_steps=10,
        fp16=args.fp16,
        report_to='none'
    )

    trainer = Trainer(
        model=model,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
        args=training_args
    )

    trainer.train()
    trainer.save_model(args.output)
    print(f"LoRA weights saved to {args.output}")

    # Update last trained count
    last_count_file.write_text(str(total_prompts))

if __name__ == "__main__":
    main()
