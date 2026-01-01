"""Business Builder agent - handles business design and strategy tasks."""
from typing import Dict, Any
from openai import OpenAI

from app.settings import settings


class BusinessBuilderAgent:
    """Agent specialized in business model design, positioning, and strategy."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.model = settings.openai_model
    
    def generate_concepts(self, build_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate 3 business concepts based on build spec."""
        system_msg = """You are a business strategy expert specializing in online businesses.
Your job is to generate practical, automation-friendly business concepts optimized for:
- Digital delivery
- Low customer support burden
- Subscription or repeatable revenue
- Clear ROI for customers
- Minimal ongoing content treadmill

Be specific and implementation-focused."""

        user_msg = f"""Based on this Build Spec, propose 3 business concepts:

{build_spec}

For each concept include:
1) What it is (1 sentence)
2) Who buys it (ICP)
3) Pain it solves + measurable outcome
4) Why it can be low-touch (automation + boundaries)
5) Competitive moat
6) Pricing ladder (entry / core / premium)
7) 2 acquisition channels
8) MVP scope (can ship in 14 days)
9) Biggest risks + mitigation

End with a recommendation of ONE concept to pursue and why.

Format as JSON with this structure:
{{
  "concepts": [
    {{
      "title": "...",
      "description": "...",
      "icp": "...",
      "pain_solved": "...",
      "measurable_outcome": "...",
      "low_touch_rationale": "...",
      "competitive_moat": "...",
      "pricing_ladder": [...],
      "acquisition_channels": [...],
      "mvp_scope": "...",
      "risks": [...]
    }}
  ],
  "recommendation": {{
    "concept_index": 0,
    "rationale": "..."
  }}
}}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.8,
            max_tokens=4096,
        )
        
        return {"response": response.choices[0].message.content}
    
    def create_positioning(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create competitive positioning and wedge."""
        system_msg = """You are a positioning strategist. Create sharp, differentiated positioning
that makes the product stand out in a crowded market."""

        user_msg = f"""Create competitive positioning for this concept:

{concept}

Deliver:
- 10 competitor/alternative categories
- What they promise
- Where they fail (gaps)
- A positioning wedge: "Only [product] does X for Y without Z"
- 5 unique mechanisms
- 10 tagline options
- 10 domain name ideas

Format as structured JSON."""
        
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
    
    def design_offer(self, concept: Dict[str, Any], positioning: Dict[str, Any]) -> Dict[str, Any]:
        """Design the core offer with boundaries."""
        system_msg = """You are a direct-response copywriter and product designer.
Create offers that are irresistible yet have clear boundaries to prevent support overload."""

        user_msg = f"""Design the core offer for this business:

Concept: {concept}
Positioning: {positioning}

Include:
- Outcome promise (specific + measurable)
- What's included
- What's NOT included (support boundaries)
- Onboarding flow (10 minutes max)
- Time-to-value (first win in <30 minutes)
- Proof without proof strategy
- Risk reversal (guarantee that won't get abused)
- Pricing recommendation (3 tiers)
- FAQ that prevents support tickets

Write it like a product page outline in JSON format."""
        
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
    
    def write_copy(self, offer: Dict[str, Any], page_type: str = "home") -> Dict[str, Any]:
        """Write high-converting copy for website pages."""
        system_msg = """You are a conversion copywriter. Write clear, punchy copy that:
- Speaks to one ICP
- Focuses on outcome, speed, ROI
- Is scannable and trustworthy
- Avoids hype and fluff"""

        if page_type == "home":
            user_msg = f"""Write the full Home page copy for this offer:

{offer}

Include:
- Hero (headline + subheadline)
- Problem agitation
- Solution
- How it works
- Features-to-benefits
- Social proof placeholders
- Pricing teaser
- FAQ
- Final CTA

Deliver in clean Markdown with section headers."""
        
        elif page_type == "pricing":
            user_msg = f"""Write the Pricing page copy for this offer:

{offer}

Include:
- Tier names + who each tier is for
- Feature comparison list
- "Choose this if..." bullets
- Add-ons (if any)
- Guarantee copy
- Objection handling
- FAQ

Deliver in clean Markdown."""
        
        else:
            user_msg = f"Write {page_type} page copy for: {offer}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=4096,
        )
        
        return {"response": response.choices[0].message.content}
