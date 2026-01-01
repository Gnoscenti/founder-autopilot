"""Paperwork agent - automates document generation and form pre-filling."""
from typing import Dict, Any, List, Optional
from openai import OpenAI
from pathlib import Path
from datetime import datetime
import json


class PaperworkAgent:
    """Agent specialized in generating legal documents and pre-filling forms."""
    
    def __init__(
        self,
        openai_api_key: str,
        openai_api_base: str,
        openai_model: str
    ):
        self.client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
        self.model = openai_model
    
    def _call_llm(self, system: str, user: str) -> str:
        """Call LLM for document generation."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=0.3,  # Lower temperature for legal/formal content
                max_tokens=4096,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Legal Documents
    
    def generate_operating_agreement(
        self,
        business_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate LLC Operating Agreement draft."""
        
        system = """You are a business attorney. Generate comprehensive legal document drafts.
Include standard clauses and clear section headers. Mark areas requiring customization with [CUSTOMIZE]."""

        user = f"""Generate an LLC Operating Agreement draft for:

Business Name: {business_info.get('name')}
State: {business_info.get('state', 'Delaware')}
Members: {business_info.get('members', [])}
Management Structure: {business_info.get('management', 'member-managed')}

Include:
- Article I: Organization
- Article II: Purpose
- Article III: Members and Ownership
- Article IV: Management
- Article V: Capital Contributions
- Article VI: Distributions
- Article VII: Transfer of Membership Interests
- Article VIII: Dissolution
- Article IX: Miscellaneous

Format in Markdown with clear sections.
Add disclaimer: "This is a draft template. Consult with a licensed attorney before use."
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "operating_agreement",
            "content": content,
            "disclaimer": "This is a draft template. Consult with a licensed attorney before use."
        }
    
    def generate_privacy_policy(
        self,
        business_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Privacy Policy draft."""
        
        system = """You are a privacy compliance expert. Generate comprehensive privacy policies
that cover GDPR, CCPA, and general best practices."""

        user = f"""Generate a Privacy Policy for:

Business Name: {business_info.get('name')}
Website: {business_info.get('website')}
Services: {business_info.get('services', 'SaaS platform')}
Data Collected: {business_info.get('data_collected', ['email', 'name', 'usage data'])}
Third-party Services: {business_info.get('third_party', ['Stripe', 'Google Analytics'])}

Include:
1. Information We Collect
2. How We Use Your Information
3. Data Sharing and Disclosure
4. Data Security
5. Your Rights (GDPR/CCPA)
6. Cookies and Tracking
7. Children's Privacy
8. Changes to This Policy
9. Contact Information

Format in Markdown.
Add disclaimer: "This is a template. Consult with a privacy attorney for compliance."
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "privacy_policy",
            "content": content,
            "disclaimer": "This is a template. Consult with a privacy attorney for compliance."
        }
    
    def generate_terms_of_service(
        self,
        business_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Terms of Service draft."""
        
        system = """You are a business attorney. Generate comprehensive Terms of Service
that protect the business while being fair to users."""

        user = f"""Generate Terms of Service for:

Business Name: {business_info.get('name')}
Service Type: {business_info.get('service_type', 'SaaS')}
Pricing Model: {business_info.get('pricing_model', 'subscription')}
Refund Policy: {business_info.get('refund_policy', '30-day money-back guarantee')}

Include:
1. Acceptance of Terms
2. Description of Service
3. User Accounts and Registration
4. Payment Terms
5. Refund Policy
6. User Conduct and Prohibited Uses
7. Intellectual Property
8. Disclaimers and Limitations of Liability
9. Indemnification
10. Termination
11. Governing Law
12. Changes to Terms
13. Contact Information

Format in Markdown.
Add disclaimer: "This is a template. Consult with an attorney before use."
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "terms_of_service",
            "content": content,
            "disclaimer": "This is a template. Consult with an attorney before use."
        }
    
    def generate_refund_policy(
        self,
        business_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate Refund Policy."""
        
        system = """You are a customer service expert. Generate clear, fair refund policies
that balance customer satisfaction with business protection."""

        user = f"""Generate a Refund Policy for:

Business: {business_info.get('name')}
Product Type: {business_info.get('product_type', 'digital product')}
Refund Window: {business_info.get('refund_window', '30 days')}
Conditions: {business_info.get('conditions', [])}

Include:
- Eligibility criteria
- Refund process
- Timeframe for refunds
- Exceptions
- Contact information

Format in clear, customer-friendly language.
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "refund_policy",
            "content": content
        }
    
    # Business Formation Documents
    
    def generate_business_plan_outline(
        self,
        business_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate business plan outline."""
        
        system = """You are a business consultant. Create comprehensive business plan outlines
suitable for investors, lenders, or internal planning."""

        user = f"""Generate a business plan outline for:

{json.dumps(business_spec, indent=2)}

Include:
1. Executive Summary
2. Company Description
3. Market Analysis
4. Organization and Management
5. Service/Product Line
6. Marketing and Sales Strategy
7. Financial Projections
8. Funding Requirements (if applicable)
9. Appendix

For each section, provide:
- Key questions to answer
- Data/research needed
- Recommended length

Format in Markdown.
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "business_plan_outline",
            "content": content
        }
    
    def pre_fill_llc_formation(
        self,
        business_info: Dict[str, Any],
        state: str = "Delaware"
    ) -> Dict[str, Any]:
        """Pre-fill LLC formation documents."""
        
        system = """You are a business formation specialist. Generate pre-filled forms
for LLC formation, marking fields that require human review with [REVIEW]."""

        user = f"""Pre-fill LLC formation documents for {state}:

Business Information:
{json.dumps(business_info, indent=2)}

Generate:
1. Certificate of Formation / Articles of Organization
2. Registered Agent Information
3. Initial Member/Manager Information
4. EIN Application (Form SS-4) preparation checklist

For each document:
- Fill in all available information
- Mark uncertain fields with [REVIEW]
- Include filing instructions
- List required fees
- Provide state filing website

Format as structured data (JSON) with instructions.
"""
        
        response = self._call_llm(system, user)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            forms = json.loads(response[json_start:json_end])
            
            return {
                "success": True,
                "state": state,
                "forms": forms,
                "next_steps": [
                    "Review all [REVIEW] fields",
                    "Verify information accuracy",
                    "Visit state filing website",
                    "Complete payment",
                    "Submit forms"
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e), "raw_response": response}
    
    # Tax and Compliance
    
    def generate_tax_checklist(
        self,
        business_type: str,
        state: str
    ) -> Dict[str, Any]:
        """Generate tax compliance checklist."""
        
        system = """You are a tax advisor. Create comprehensive tax compliance checklists
for small businesses."""

        user = f"""Generate a tax compliance checklist for:

Business Type: {business_type}
State: {state}

Include:
- Federal tax obligations (EIN, estimated taxes, annual filing)
- State tax obligations
- Local tax obligations
- Important deadlines
- Required forms
- Recommended accounting practices
- When to hire a CPA

Format as actionable checklist in Markdown.
Add disclaimer: "This is general information. Consult with a tax professional."
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "tax_checklist",
            "content": content,
            "disclaimer": "This is general information. Consult with a tax professional."
        }
    
    # Contracts and Agreements
    
    def generate_service_agreement(
        self,
        service_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate service agreement template."""
        
        system = """You are a contracts attorney. Generate professional service agreements
that clearly define scope, terms, and protections for both parties."""

        user = f"""Generate a Service Agreement for:

Service Provider: {service_details.get('provider')}
Client: {service_details.get('client', '[CLIENT NAME]')}
Services: {service_details.get('services')}
Duration: {service_details.get('duration')}
Payment Terms: {service_details.get('payment_terms')}

Include:
1. Parties
2. Services to be Provided
3. Term and Termination
4. Payment Terms
5. Intellectual Property Rights
6. Confidentiality
7. Warranties and Disclaimers
8. Limitation of Liability
9. Dispute Resolution
10. General Provisions

Format in Markdown.
Add disclaimer: "This is a template. Have an attorney review before use."
"""
        
        content = self._call_llm(system, user)
        
        return {
            "success": True,
            "document_type": "service_agreement",
            "content": content,
            "disclaimer": "This is a template. Have an attorney review before use."
        }
    
    # Document Package Generation
    
    def generate_startup_legal_package(
        self,
        business_info: Dict[str, Any],
        output_dir: str
    ) -> Dict[str, Any]:
        """Generate complete legal document package for startup."""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        documents = []
        
        # 1. Operating Agreement
        doc = self.generate_operating_agreement(business_info)
        if doc["success"]:
            file_path = output_path / "operating_agreement.md"
            file_path.write_text(doc["content"], encoding='utf-8')
            documents.append({"type": "operating_agreement", "file": str(file_path)})
        
        # 2. Privacy Policy
        doc = self.generate_privacy_policy(business_info)
        if doc["success"]:
            file_path = output_path / "privacy_policy.md"
            file_path.write_text(doc["content"], encoding='utf-8')
            documents.append({"type": "privacy_policy", "file": str(file_path)})
        
        # 3. Terms of Service
        doc = self.generate_terms_of_service(business_info)
        if doc["success"]:
            file_path = output_path / "terms_of_service.md"
            file_path.write_text(doc["content"], encoding='utf-8')
            documents.append({"type": "terms_of_service", "file": str(file_path)})
        
        # 4. Refund Policy
        doc = self.generate_refund_policy(business_info)
        if doc["success"]:
            file_path = output_path / "refund_policy.md"
            file_path.write_text(doc["content"], encoding='utf-8')
            documents.append({"type": "refund_policy", "file": str(file_path)})
        
        # 5. Tax Checklist
        doc = self.generate_tax_checklist(
            business_info.get('business_type', 'LLC'),
            business_info.get('state', 'Delaware')
        )
        if doc["success"]:
            file_path = output_path / "tax_checklist.md"
            file_path.write_text(doc["content"], encoding='utf-8')
            documents.append({"type": "tax_checklist", "file": str(file_path)})
        
        # Generate summary
        summary = f"""# Startup Legal Package

Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Documents Included

{chr(10).join([f"- {doc['type']}: {doc['file']}" for doc in documents])}

## Important Disclaimers

⚠️ **These are template documents for informational purposes only.**

- NOT legal advice
- NOT a substitute for an attorney
- State laws vary significantly
- Review and customize for your specific situation
- Have an attorney review before use

## Next Steps

1. **Review all documents carefully**
   - Check all [CUSTOMIZE] and [REVIEW] markers
   - Verify information accuracy
   - Ensure compliance with your state laws

2. **Consult with professionals**
   - Attorney: Review legal documents
   - CPA: Tax planning and compliance
   - Insurance agent: Business insurance needs

3. **File required documents**
   - State business formation
   - EIN application (IRS)
   - State tax registration
   - Local business licenses

4. **Implement policies**
   - Add privacy policy to website
   - Include ToS in signup flow
   - Train team on compliance

## Resources

- State Business Filing: [Your state's Secretary of State website]
- IRS EIN Application: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online
- Legal Aid: https://www.lsc.gov/what-legal-aid/find-legal-aid
"""
        
        summary_file = output_path / "README.md"
        summary_file.write_text(summary, encoding='utf-8')
        
        return {
            "success": True,
            "documents": documents,
            "summary_file": str(summary_file),
            "output_dir": str(output_path)
        }
