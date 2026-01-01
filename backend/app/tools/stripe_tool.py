"""Stripe tool - payment and subscription management."""
from typing import Dict, Any, Optional
import stripe

from app.core.vault import get_stripe_key


class StripeTool:
    """Tool for Stripe operations."""
    
    def __init__(self):
        stripe_key = get_stripe_key()
        if stripe_key:
            stripe.api_key = stripe_key
    
    def create_product(self, name: str, description: str) -> Dict[str, Any]:
        """Create a Stripe product."""
        if not stripe.api_key:
            return {"success": False, "error": "Stripe API key not configured"}
        
        try:
            product = stripe.Product.create(
                name=name,
                description=description,
            )
            return {"success": True, "product_id": product.id, "product": product}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_price(
        self,
        product_id: str,
        amount: int,
        currency: str = "usd",
        interval: str = "month"
    ) -> Dict[str, Any]:
        """Create a Stripe price."""
        if not stripe.api_key:
            return {"success": False, "error": "Stripe API key not configured"}
        
        try:
            price = stripe.Price.create(
                product=product_id,
                unit_amount=amount,
                currency=currency,
                recurring={"interval": interval},
            )
            return {"success": True, "price_id": price.id, "price": price}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_products(self) -> Dict[str, Any]:
        """List all products."""
        if not stripe.api_key:
            return {"success": False, "error": "Stripe API key not configured"}
        
        try:
            products = stripe.Product.list(limit=100)
            return {"success": True, "products": products.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
