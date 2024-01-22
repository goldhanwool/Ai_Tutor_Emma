# import torch
# from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# async def huggingface_call(text):
#     # Load tokenizer
#     tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
#     # Load model
#     model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
#     # Create tokens - number representation of our text
#     tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
#     summary = model.generate(**tokens)
#     summary_text = tokenizer.decode(summary[0])
#     print("[huggingface_call] > summary_text: ", summary_text)
#     return summary_text