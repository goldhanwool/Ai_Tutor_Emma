import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def huggingface_call(text):
    # Load tokenizer
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
    # Load model
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    # Create tokens - number representation of our text
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    summary = model.generate(**tokens)
    summary_text = tokenizer.decode(summary[0])
    print("\n[huggingface_call] > summary_text: ", summary_text)
    return summary_text


text = """
"a word that asserts or declares; that part of speech of which the office is predication, and which, either alone or with various modifiers or adjuncts, combines with a subject to make a sentence" [Century Dictionary], late 14c., from Old French verbe "word; word of God; saying; part of speech that expresses action or being" (12c.) and directly from Latin verbum "verb," originally "a word," from PIE root *were- (3) "to speak" (source also of Avestan urvata- "command;" Sanskrit vrata- "command, vow;" Greek rhētōr "public speaker," rhetra "agreement, covenant," eirein "to speak, say;" Hittite weriga- "call, summon;" Lithuanian vardas "name;" Gothic waurd, Old English word "word").
"""
huggingface_call(text)
