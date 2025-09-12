import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_model', type=str, required=True, help='Path to the base LLaMA model')
    parser.add_argument('--data', type=str, required=True, help='Path to JSON/CSV file with training prompts')
    parser.add_argument('--output', type=str, default='./lora_weights', help='Output path for LoRA weights')
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--epochs', type=int, default=3)
    parser.add_argument('--fp16', action='store_true')
    args = parser.parse_args()

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        device_map='auto',
        load_in_4bit=True,
        torch_dtype=torch.float16
    )

    # Load dataset
    dataset = load_dataset('json', data_files=args.data)
    def tokenize(example):
        return tokenizer(example['prompt'], truncation=True, padding='max_length', max_length=512)
    tokenized_dataset = dataset.map(tokenize, batched=True)

    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

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
        train_dataset=tokenized_dataset['train'],
        tokenizer=tokenizer,
        data_collator=data_collator,
        args=training_args
    )

    trainer.train()
    trainer.save_model(args.output)
    print(f"LoRA weights saved to {args.output}")

if __name__ == "__main__":
    main()
