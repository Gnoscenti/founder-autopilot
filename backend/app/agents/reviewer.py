"""Reviewer agent - quality assurance and critique."""
from typing import Dict, Any
from openai import OpenAI

from app.settings import settings


class ReviewerAgent:
    """Agent specialized in reviewing and improving outputs."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.model = settings.openai_model
    
    def review_offer(self, offer: Dict[str, Any]) -> Dict[str, Any]:
        """Brutally review and improve an offer."""
        system_msg = """You are a skeptical buyer and top direct-response strategist.
Your job is to tear apart offers and then fix them to be irresistible."""

        user_msg = f"""Act as a skeptical buyer. Tear down this offer:

{offer}

Then rewrite:
- Headline
- Promise
- Tiers
- Guarantee
- Top 10 FAQs

Be brutally honest about weaknesses, then provide superior alternatives.

Format as JSON with critique and improvements."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.8,
            max_tokens=3072,
        )
        
        return {"response": response.choices[0].message.content}
    
    def polish_copy(self, copy: str) -> Dict[str, Any]:
        """Polish copy to sound professional and trustworthy."""
        system_msg = """You are a copy editor. Polish copy to sound trustworthy, modern, and professional.
Improve scannability without losing persuasive power. Avoid hype."""

        user_msg = f"""Polish this copy:

{copy}

Make it:
- More trustworthy
- More scannable
- More professional
- Less hypey

Return revised copy + list of specific changes made.

Format as JSON."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.5,
            max_tokens=3072,
        )
        
        return {"response": response.choices[0].message.content}
    
    def audit_risks(self, business_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive risk audit."""
        system_msg = """You are a risk management consultant. Identify and assess risks across:
legal, financial, operational, reputational, and technical dimensions."""

        user_msg = f"""Run a risk audit for this business:

{business_spec}

For each risk category (legal, refund/chargeback, platform dependency, 
privacy/data, claim substantiation, reputational), identify:
- Specific risks
- Severity (1-5)
- Likelihood (1-5)
- Mitigation strategies

Format as JSON with structured risk assessment."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.6,
            max_tokens=3072,
        )
        
        return {"response": response.choices[0].message.content}
