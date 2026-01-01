"""Marketing agent - handles go-to-market strategy and execution."""
from typing import Dict, Any
from openai import OpenAI

from app.settings import settings


class MarketingAgent:
    """Agent specialized in marketing strategy and execution."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.model = settings.openai_model
    
    def create_channel_plan(self, business_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create focused go-to-market plan for one channel."""
        system_msg = """You are a growth marketing strategist. Create practical, execution-focused
marketing plans that prioritize speed to revenue and compounding effects."""

        user_msg = f"""Choose ONE primary acquisition channel for the first 60 days and create
a detailed execution plan.

Business: {business_spec}

Justify the channel choice with:
- Speed to revenue
- Cost
- Compounding effects
- Fit with the business

Then provide a 60-day execution plan with weekly deliverables.

Format as JSON with clear action items."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=3072,
        )
        
        return {"response": response.choices[0].message.content}
    
    def create_seo_plan(self, business_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create topical authority SEO plan."""
        system_msg = """You are an SEO strategist focused on topical authority and conversion."""

        user_msg = f"""Create an SEO plan for:

{business_spec}

Include:
- 6 pillar pages
- 30 supporting posts
- Internal linking map
- CTA placement strategy
- Lead magnet placements
- Money pages and content funnel

Provide 5 example outlines for highest-intent posts.

Format as JSON."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=3072,
        )
        
        return {"response": response.choices[0].message.content}
    
    def create_email_sequence(self, lead_magnet: Dict[str, Any]) -> Dict[str, Any]:
        """Create email nurture sequence."""
        system_msg = """You are an email marketing expert. Write conversion-focused email sequences
that deliver value and naturally transition to the offer."""

        user_msg = f"""Create a 5-email sequence for this lead magnet:

{lead_magnet}

Each email should:
- Deliver value
- Build trust
- Naturally lead to the paid offer
- Have clear CTAs

Format as JSON with subject lines and body copy."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=3072,
        )
        
        return {"response": response.choices[0].message.content}
