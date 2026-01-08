"""
Vision-Language Model for generating engineering explanations of defects.
Uses BLIP-2 to analyze cropped defect regions and provide professional assessments.
"""

from typing import Dict, Any
from PIL import Image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration


class VisionLanguageModel:
    """
    BLIP-2 based vision-language model for defect explanation generation.

    Generates engineering-grade natural language explanations for detected defects.
    """

    def __init__(self, model_name: str = "Salesforce/blip2-opt-2.7b", device: str = None):
        """
        Initialize the Vision-Language Model.

        Args:
            model_name: Hugging Face model identifier for BLIP-2
            device: Device to run model on ('cuda', 'mps', or 'cpu')
        """
        # Auto-detect device if not specified
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device

        print(f"Loading Vision-Language Model on {self.device}...")

        # Load BLIP-2 processor and model
        self.processor = Blip2Processor.from_pretrained(model_name)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        self.model.to(self.device)
        self.model.eval()

        print("Vision-Language Model loaded successfully")

    def generate_explanation(
        self,
        image: Image.Image,
        defect_type: str,
        severity: str
    ) -> Dict[str, str]:
        """
        Generate engineering explanation and recommended action for a defect.

        Args:
            image: Cropped image of the defect region
            defect_type: Type of defect (crack, corrosion, spalling)
            severity: Severity level (Low, Medium, High)

        Returns:
            Dictionary containing:
                - explanation: Technical description of the defect
                - recommended_action: Engineering recommendation
        """
        # Create engineering-focused prompts
        explanation_prompt = self._create_explanation_prompt(defect_type, severity)
        action_prompt = self._create_action_prompt(defect_type, severity)

        # Generate explanation
        explanation = self._generate_text(image, explanation_prompt)

        # Generate recommended action
        recommended_action = self._generate_text(image, action_prompt)

        return {
            "explanation": explanation.strip(),
            "recommended_action": recommended_action.strip()
        }

    def _create_explanation_prompt(self, defect_type: str, severity: str) -> str:
        """
        Create a prompt for generating technical explanation.
        """
        base_prompt = (
            f"You are a structural inspection engineer analyzing a {severity.lower()} severity "
            f"{defect_type} defect. Describe the structural condition and potential risk factors "
            f"in technical terms. Be concise and professional."
        )
        return f"Question: {base_prompt} Answer:"

    def _create_action_prompt(self, defect_type: str, severity: str) -> str:
        """
        Create a prompt for generating recommended actions.
        """
        base_prompt = (
            f"You are a structural inspection engineer. For this {severity.lower()} severity "
            f"{defect_type}, provide a specific recommended action for maintenance or repair. "
            f"Be direct and actionable."
        )
        return f"Question: {base_prompt} Answer:"

    def _generate_text(self, image: Image.Image, prompt: str, max_length: int = 100) -> str:
        """
        Generate text from image and prompt using BLIP-2.

        Args:
            image: PIL Image
            prompt: Text prompt
            max_length: Maximum length of generated text

        Returns:
            Generated text
        """
        # Prepare inputs
        inputs = self.processor(image, prompt, return_tensors="pt")

        # Move inputs to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Generate text
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=3,
                temperature=0.7,
                do_sample=False
            )

        # Decode generated text
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text

    def generate_simple_explanation(
        self,
        defect_type: str,
        severity: str
    ) -> Dict[str, str]:
        """
        Generate rule-based explanation when VLM is unavailable or for faster inference.
        Fallback method for production scenarios.

        Args:
            defect_type: Type of defect
            severity: Severity level

        Returns:
            Dictionary with explanation and recommended_action
        """
        explanations = {
            "crack": {
                "High": {
                    "explanation": "Significant linear discontinuity detected in structural element. The crack extent suggests potential load path disruption or material fatigue. Location and propagation pattern indicate need for immediate structural assessment.",
                    "recommended_action": "Conduct detailed structural evaluation including load capacity analysis. Consider temporary shoring if needed. Implement crack monitoring system and develop repair specifications with licensed structural engineer."
                },
                "Medium": {
                    "explanation": "Moderate crack formation observed in structural component. The defect exhibits characteristics of early-stage material degradation or settlement-induced stress. Current extent suggests localized rather than systemic issue.",
                    "recommended_action": "Install crack width monitoring gauges. Perform material testing to determine cause. Schedule repair using appropriate epoxy injection or routing and sealing within next maintenance cycle."
                },
                "Low": {
                    "explanation": "Minor surface crack detected. Defect appears superficial with limited propagation. Likely caused by shrinkage, thermal stress, or minor settlement. No immediate structural concern evident.",
                    "recommended_action": "Document crack location and dimensions. Apply surface sealant to prevent moisture ingress. Schedule for re-inspection in 6-12 months to monitor for progression."
                }
            },
            "corrosion": {
                "High": {
                    "explanation": "Advanced corrosion detected with evidence of significant material loss. The deterioration pattern suggests prolonged exposure to corrosive environment. Potential for reduced load-bearing capacity and progressive structural degradation.",
                    "recommended_action": "Immediate structural assessment required. Perform material thickness testing and load capacity evaluation. Implement corrosion protection system. Plan for member replacement or structural reinforcement as engineering analysis dictates."
                },
                "Medium": {
                    "explanation": "Moderate corrosion identified on structural surface. Observable oxidation with partial material degradation. Current state indicates active corrosion process requiring intervention to prevent acceleration.",
                    "recommended_action": "Remove corrosion products and assess remaining material thickness. Apply protective coating system per SSPC standards. Improve drainage or ventilation to eliminate moisture source. Monitor quarterly for progression."
                },
                "Low": {
                    "explanation": "Surface-level corrosion detected with minimal material loss. Early-stage oxidation present, primarily affecting protective coating or superficial material layers. Structural integrity currently maintained.",
                    "recommended_action": "Clean affected area and apply corrosion inhibitor. Restore protective coating system. Address moisture source if identified. Include in routine inspection schedule."
                }
            },
            "spalling": {
                "High": {
                    "explanation": "Extensive concrete spalling with visible material loss detected. Defect severity suggests potential reinforcement exposure or advanced deterioration. Pattern indicates freeze-thaw damage, corrosion-induced pressure, or alkali-silica reaction.",
                    "recommended_action": "Urgent engineering assessment required. Remove loose material and inspect for reinforcement corrosion. Perform concrete strength testing. Execute structural repair using compatible materials per ACI 546 guidelines. Address root cause of deterioration."
                },
                "Medium": {
                    "explanation": "Moderate spalling observed with measurable concrete delamination. Surface layer failure evident, potentially due to reinforcement corrosion, freeze-thaw cycles, or construction defects. Underlying structure requires verification.",
                    "recommended_action": "Remove delaminated concrete and assess extent of damage. Test for chloride content and carbonation depth. Repair using polymer-modified concrete or appropriate patching material. Implement preventive measures for underlying cause."
                },
                "Low": {
                    "explanation": "Minor surface spalling detected affecting concrete cover. Limited material loss observed, likely due to localized impact, minor freeze-thaw action, or finishing issues. Structural reinforcement not compromised.",
                    "recommended_action": "Remove loose material and clean surface. Apply concrete patching compound for affected areas. Seal surface to prevent moisture penetration. Monitor during regular inspections."
                }
            }
        }

        defect_type_lower = defect_type.lower()

        if defect_type_lower in explanations and severity in explanations[defect_type_lower]:
            return explanations[defect_type_lower][severity]
        else:
            return {
                "explanation": f"{severity} severity {defect_type} detected requiring engineering assessment.",
                "recommended_action": "Consult with licensed structural engineer for evaluation and repair recommendations."
            }
