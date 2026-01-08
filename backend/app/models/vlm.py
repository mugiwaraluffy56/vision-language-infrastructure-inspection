from transformers import BlipProcessor, Blip2ForConditionalGeneration
from PIL import Image
import torch

class VLMClient:
    def __init__(self, model_id: str = "Salesforce/blip2-opt-2.7b"):
        """
        Initialize the VLM client.
        Using Salesforce/blip2-opt-2.7b as a good trade-off for MVP.
        """
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        # Lazy loading or simple init. For MVP we load at startup or on first request?
        # Better to load on init but print strict warnings.
        print(f"Loading VLM model: {model_id} on {self.device}...")
        try:
            self.processor = BlipProcessor.from_pretrained(model_id)
            # Use float16 if on GPU for memory saving
            torch_dtype = torch.float16 if self.device != "cpu" else torch.float32
            self.model = Blip2ForConditionalGeneration.from_pretrained(
                model_id, torch_dtype=torch_dtype
            )
            self.model.to(self.device)
            print("VLM model loaded successfully.")
        except Exception as e:
            print(f"Error loading VLM model: {e}")
            print("Running in MOCK VLM mode for MVP demonstration.")
            self.model = None

    def generate_explanation(self, image: Image.Image, defect_type: str, severity: str) -> str:
        """
        Generate an engineering explanation for the defect.
        """
        prompt = (
            f"Question: You are a structural inspection engineer. "
            f"This is a {severity} severity {defect_type}. "
            f"Explain the structural risk and recommended action for the defect shown. Answer:"
        )

        if self.model is None:
             # Mock response if model failed to load (e.g. no internet or disk space)
             return (
                 f"Detected {severity} severity {defect_type}. "
                 f"Structural integrity may be compromised depending on load path. "
                 f"Recommendation: Monitor growth and verify with NDT."
             )

        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device, self.model.dtype)
        
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=50)
            explanation = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        
        return explanation
