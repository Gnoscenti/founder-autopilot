"""Web Development agent - builds and deploys websites."""
from typing import Dict, Any
from openai import OpenAI

from app.settings import settings


class WebDevAgent:
    """Agent specialized in web development and deployment."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.model = settings.openai_model
    
    def generate_website_plan(self, copy: Dict[str, Any], brand: Dict[str, Any]) -> Dict[str, Any]:
        """Generate website architecture and implementation plan."""
        system_msg = """You are a web developer specializing in conversion-focused landing pages.
Create practical, modern web implementations using Next.js, React, and TailwindCSS."""

        user_msg = f"""Create a website implementation plan:

Copy: {copy}
Brand: {brand}

Include:
- Page structure and components
- Tech stack recommendations
- Deployment strategy (Vercel/Netlify)
- Integration points (Stripe, email, analytics)
- Performance optimizations
- SEO basics

Format as JSON with clear implementation steps."""
        
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
    
    def generate_component_code(self, component_spec: Dict[str, Any]) -> str:
        """Generate React component code."""
        system_msg = """You are an expert React developer. Generate clean, modern React components
using TypeScript and TailwindCSS. Follow best practices and accessibility guidelines."""

        user_msg = f"""Generate a React component for:

{component_spec}

Use TypeScript and TailwindCSS. Make it responsive and accessible."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        
        return response.choices[0].message.content
