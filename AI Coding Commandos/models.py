from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

# Initialize models
triage_model = pipeline("text-classification", model="bert-base-uncased")
emotion_model = pipeline("sentiment-analysis")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def triage_case(user_input):
    try:
        result = triage_model(user_input)
        label = result[0]['label']
        if label.lower() == 'urgent':
            return "High-risk case detected. Immediate human intervention required."
        else:
            return "Case logged. Follow the next steps to provide more details."
    except Exception as e:
        return f"Error in triage: {str(e)}"

def detect_emotion(text):
    try:
        result = emotion_model(text)
        return result[0]['label']
    except Exception as e:
        return f"Error in emotion detection: {str(e)}"

def generate_legal_document(input_text):
    try:
        inputs = gpt2_tokenizer.encode(input_text, return_tensors="pt")
        outputs = gpt2_model.generate(
            inputs, 
            max_length=500, 
            do_sample=True, 
            top_k=50, 
            top_p=0.95, 
            temperature=0.7
        )
        return gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error in document generation: {str(e)}"
