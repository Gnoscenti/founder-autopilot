"""Stripe agent - handles payment setup and configuration."""
from typing import Dict, Any, Optional
import stripe
from openai import OpenAI

from app.settings import settings
from app.core.vault import get_stripe_key


class StripeAgent:
    """Agent specialized in Stripe payment integration."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.model = settings.openai_model
        
        # Initialize Stripe
        stripe_key = get_stripe_key()
        if stripe_key:
            stripe.api_key = stripe_key
    
    def plan_stripe_setup(self, pricing_tiers: list) -> Dict[str, Any]:
        """Plan Stripe product and price setup."""
        system_msg = """You are a Stripe integration expert. Plan the optimal Stripe setup
for subscription products, including products, prices, and webhooks."""

        user_msg = f"""Plan Stripe setup for these pricing tiers:

{pricing_tiers}

Include:
- Product structure
- Price IDs (monthly/annual)
- Recommended features per tier
- Webhook events to handle
- Subscription entitlement logic
- Trial period recommendations

Format as JSON."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.5,
            max_tokens=2048,
        )
        
        return {"response": response.choices[0].message.content}
    
    def create_product(self, name: str, description: str) -> Optional[str]:
        """Create a Stripe product (requires API key)."""
        if not stripe.api_key:
            return None
        
        try:
            product = stripe.Product.create(
                name=name,
                description=description,
            )
            return product.id
        except Exception as e:
            print(f"Error creating Stripe product: {e}")
            return None
    
    def create_price(
        self,
        product_id: str,
        amount: int,
        currency: str = "usd",
        interval: str = "month"
    ) -> Optional[str]:
        """Create a Stripe price (requires API key)."""
        if not stripe.api_key:
            return None
        
        try:
            price = stripe.Price.create(
                product=product_id,
                unit_amount=amount,
                currency=currency,
                recurring={"interval": interval},
            )
            return price.id
        except Exception as e:
            print(f"Error creating Stripe price: {e}")
            return None
