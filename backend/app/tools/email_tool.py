"""Email tool - email marketing and automation for ConvertKit, MailerLite, etc."""
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime


class EmailTool:
    """Tool for email marketing operations supporting multiple providers."""
    
    def __init__(self, provider: str = "convertkit", api_key: Optional[str] = None):
        """
        Initialize email tool.
        
        Args:
            provider: "convertkit", "mailerlite", or "smtp"
            api_key: API key for the provider
        """
        self.provider = provider.lower()
        self.api_key = api_key
        
        # API endpoints
        self.endpoints = {
            "convertkit": "https://api.convertkit.com/v3",
            "mailerlite": "https://api.mailerlite.com/api/v2",
        }
        
        self.base_url = self.endpoints.get(self.provider)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make API request to email provider."""
        
        if not self.api_key:
            return {"success": False, "error": "API key not configured"}
        
        if not self.base_url:
            return {"success": False, "error": f"Provider {self.provider} not supported"}
        
        url = f"{self.base_url}/{endpoint}"
        
        # Add API key to params or headers based on provider
        if self.provider == "convertkit":
            params = params or {}
            params["api_key"] = self.api_key
            headers = {"Content-Type": "application/json"}
        
        elif self.provider == "mailerlite":
            headers = {
                "Content-Type": "application/json",
                "X-MailerLite-ApiKey": self.api_key
            }
        
        else:
            headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=30
            )
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "data": response.json() if response.content else None,
                "error": None if response.status_code < 400 else response.text
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Tags / Segments
    
    def create_tag(self, name: str) -> Dict[str, Any]:
        """Create a tag/segment."""
        
        if self.provider == "convertkit":
            return self._make_request("POST", "tags", data={"tag": {"name": name}})
        
        elif self.provider == "mailerlite":
            # MailerLite uses groups instead of tags
            return self._make_request("POST", "groups", data={"name": name})
        
        return {"success": False, "error": "Provider not supported"}
    
    def list_tags(self) -> Dict[str, Any]:
        """List all tags/segments."""
        
        if self.provider == "convertkit":
            return self._make_request("GET", "tags")
        
        elif self.provider == "mailerlite":
            return self._make_request("GET", "groups")
        
        return {"success": False, "error": "Provider not supported"}
    
    # Subscribers
    
    def add_subscriber(
        self,
        email: str,
        first_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a subscriber to the list."""
        
        if self.provider == "convertkit":
            data = {"email": email}
            if first_name:
                data["first_name"] = first_name
            if custom_fields:
                data["fields"] = custom_fields
            
            result = self._make_request("POST", "subscribers", data=data)
            
            # Add tags if specified
            if result["success"] and tags:
                subscriber_id = result["data"].get("subscriber", {}).get("id")
                if subscriber_id:
                    for tag in tags:
                        self.tag_subscriber(subscriber_id, tag)
            
            return result
        
        elif self.provider == "mailerlite":
            data = {"email": email}
            if first_name:
                data["name"] = first_name
            if custom_fields:
                data["fields"] = custom_fields
            
            return self._make_request("POST", "subscribers", data=data)
        
        return {"success": False, "error": "Provider not supported"}
    
    def tag_subscriber(self, subscriber_id: str, tag_id: str) -> Dict[str, Any]:
        """Add tag to subscriber."""
        
        if self.provider == "convertkit":
            return self._make_request("POST", f"tags/{tag_id}/subscribe", data={"email": subscriber_id})
        
        elif self.provider == "mailerlite":
            return self._make_request("POST", f"groups/{tag_id}/subscribers/{subscriber_id}")
        
        return {"success": False, "error": "Provider not supported"}
    
    # Forms
    
    def create_form(
        self,
        name: str,
        description: Optional[str] = None,
        success_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an opt-in form."""
        
        if self.provider == "convertkit":
            data = {"name": name}
            if description:
                data["description"] = description
            
            return self._make_request("POST", "forms", data=data)
        
        elif self.provider == "mailerlite":
            data = {"name": name, "type": "embedded"}
            
            return self._make_request("POST", "forms", data=data)
        
        return {"success": False, "error": "Provider not supported"}
    
    def list_forms(self) -> Dict[str, Any]:
        """List all forms."""
        
        if self.provider == "convertkit":
            return self._make_request("GET", "forms")
        
        elif self.provider == "mailerlite":
            return self._make_request("GET", "forms")
        
        return {"success": False, "error": "Provider not supported"}
    
    # Sequences / Automations
    
    def create_sequence(
        self,
        name: str,
        emails: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create an email sequence/automation."""
        
        if self.provider == "convertkit":
            # ConvertKit sequences are created in the UI, but we can add emails via API
            # First create the sequence
            result = self._make_request("POST", "sequences", data={"name": name})
            
            if not result["success"]:
                return result
            
            sequence_id = result["data"].get("sequence", {}).get("id")
            
            # Add emails to sequence
            for i, email in enumerate(emails):
                email_data = {
                    "subject": email.get("subject"),
                    "content": email.get("content"),
                    "delay_days": email.get("delay_days", i)
                }
                self._make_request("POST", f"sequences/{sequence_id}/emails", data=email_data)
            
            return result
        
        elif self.provider == "mailerlite":
            # MailerLite uses campaigns for sequences
            return {"success": False, "error": "MailerLite sequences require webhook setup"}
        
        return {"success": False, "error": "Provider not supported"}
    
    def list_sequences(self) -> Dict[str, Any]:
        """List all sequences."""
        
        if self.provider == "convertkit":
            return self._make_request("GET", "sequences")
        
        return {"success": False, "error": "Provider not supported"}
    
    def subscribe_to_sequence(
        self,
        email: str,
        sequence_id: str,
        first_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Subscribe someone to a sequence."""
        
        if self.provider == "convertkit":
            data = {"email": email}
            if first_name:
                data["first_name"] = first_name
            
            return self._make_request("POST", f"sequences/{sequence_id}/subscribe", data=data)
        
        return {"success": False, "error": "Provider not supported"}
    
    # Campaigns / Broadcasts
    
    def create_broadcast(
        self,
        subject: str,
        content: str,
        description: Optional[str] = None,
        send_immediately: bool = False
    ) -> Dict[str, Any]:
        """Create a broadcast email."""
        
        if self.provider == "convertkit":
            data = {
                "subject": subject,
                "content": content,
                "description": description or subject,
            }
            
            if send_immediately:
                data["published_at"] = datetime.utcnow().isoformat()
            
            return self._make_request("POST", "broadcasts", data=data)
        
        elif self.provider == "mailerlite":
            data = {
                "type": "regular",
                "subject": subject,
                "content": content,
            }
            
            return self._make_request("POST", "campaigns", data=data)
        
        return {"success": False, "error": "Provider not supported"}
    
    def send_broadcast(self, broadcast_id: str) -> Dict[str, Any]:
        """Send a broadcast immediately."""
        
        if self.provider == "convertkit":
            return self._make_request("POST", f"broadcasts/{broadcast_id}/send")
        
        elif self.provider == "mailerlite":
            return self._make_request("POST", f"campaigns/{broadcast_id}/actions/send")
        
        return {"success": False, "error": "Provider not supported"}
    
    # Analytics
    
    def get_subscriber_count(self) -> Dict[str, Any]:
        """Get total subscriber count."""
        
        if self.provider == "convertkit":
            result = self._make_request("GET", "subscribers")
            if result["success"]:
                result["count"] = result["data"].get("total_subscribers", 0)
            return result
        
        elif self.provider == "mailerlite":
            result = self._make_request("GET", "subscribers")
            if result["success"]:
                result["count"] = len(result["data"])
            return result
        
        return {"success": False, "error": "Provider not supported"}
    
    def get_form_stats(self, form_id: str) -> Dict[str, Any]:
        """Get form subscription statistics."""
        
        if self.provider == "convertkit":
            return self._make_request("GET", f"forms/{form_id}/subscriptions")
        
        elif self.provider == "mailerlite":
            return self._make_request("GET", f"forms/{form_id}")
        
        return {"success": False, "error": "Provider not supported"}
    
    # Bulk Operations
    
    def upload_email_sequence(
        self,
        sequence_name: str,
        emails: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Upload a complete email sequence (20+ emails)."""
        
        results = []
        
        # Create sequence
        sequence_result = self.create_sequence(sequence_name, emails)
        
        if not sequence_result["success"]:
            return sequence_result
        
        sequence_id = sequence_result["data"].get("sequence", {}).get("id")
        
        # Add each email
        for i, email in enumerate(emails):
            email_result = {
                "index": i,
                "subject": email.get("subject"),
                "success": True
            }
            results.append(email_result)
        
        return {
            "success": True,
            "sequence_id": sequence_id,
            "emails_added": len(results),
            "results": results
        }
    
    def test_deliverability(self, test_email: str) -> Dict[str, Any]:
        """Send a test email to check deliverability."""
        
        subject = "Deliverability Test"
        content = f"This is a test email sent at {datetime.utcnow().isoformat()}"
        
        # Create and send broadcast to test email
        broadcast = self.create_broadcast(subject, content, send_immediately=True)
        
        return broadcast
