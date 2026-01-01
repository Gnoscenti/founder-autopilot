# Founder Autopilot - Upgrades & Features

## Recent Upgrades (v2.0)

This document details the major upgrades that transform Founder Autopilot from a concept to a production-ready business automation system.

---

## Upgrade 1: Advanced Browser Automation (Playwright)

**Purpose**: Automate tasks on platforms without APIs (Stripe dashboard, Webflow, DNS registrars, etc.)

### Features

- **Session Persistence**: Saves cookies and auth state locally so you don't re-login constantly
- **Domain Allowlisting**: Security-first approach - only operates on pre-approved domains
- **No Password Scraping**: You login normally; the agent uses your authenticated session
- **Multi-session Support**: Manage multiple browser sessions for different services

### Allowlisted Domains

- `stripe.com` - Payment setup beyond API capabilities
- `webflow.com` / `framer.com` - Website builders
- `namecheap.com` / `godaddy.com` - Domain registrars
- `cloudflare.com` - DNS management
- `vercel.com` / `netlify.com` - Deployment platforms
- `convertkit.com` / `mailerlite.com` - Email marketing
- Social platforms (LinkedIn, Twitter, Facebook)

### Usage Example

```python
from app.tools.playwright_tool import PlaywrightToolSync

tool = PlaywrightToolSync()

# Navigate to Stripe dashboard (you login once)
tool.navigate("https://dashboard.stripe.com/products", session_name="stripe")

# Agent can now automate product creation
tool.click("button[data-test='create-product']")
tool.fill("input[name='name']", "Premium Plan")
tool.fill("input[name='price']", "99")

# Session is saved automatically
tool.save_session("stripe")
```

### Security Model

- Only operates on allowlisted domains
- Sessions stored locally with 0600 permissions
- Never scrapes or stores passwords
- Human approval required for sensitive operations

---

## Upgrade 2: Google Cloud Tool

**Purpose**: Automate cloud infrastructure setup (projects, APIs, service accounts, deployments)

### Two Modes

1. **CLI Mode** (Recommended): Uses `gcloud` commands via shell
2. **API Mode**: Direct API calls using service account credentials

### Automatable Tasks

- Create GCP projects
- Enable APIs (Cloud Run, Secret Manager, Cloud Build, etc.)
- Create service accounts and keys
- Manage secrets in Secret Manager
- Deploy to Cloud Run
- Create Cloud Storage buckets
- Upload files to storage

### Usage Example

```python
from app.tools.gcloud_tool import GCloudTool

tool = GCloudTool(mode="cli")

# Create project
tool.create_project("my-saas-app", "My SaaS App")

# Enable common APIs
tool.enable_common_apis("my-saas-app")

# Create service account
tool.create_service_account(
    "backend-sa",
    "Backend Service Account",
    project_id="my-saas-app"
)

# Deploy to Cloud Run
tool.deploy_cloud_run(
    "api-service",
    "gcr.io/my-saas-app/api:latest",
    region="us-central1",
    env_vars={"DATABASE_URL": "..."}
)

# Get deployment URL
result = tool.get_cloud_run_url("api-service")
print(f"Deployed at: {result['url']}")
```

### First-time Setup

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Login (one-time, browser-based)
gcloud auth login

# Set default project
gcloud config set project my-project-id
```

---

## Upgrade 3: Website Launch Toolchain

**Purpose**: Complete automation from code generation to live website

### Full Workflow

1. **Create Next.js Project**: Modern React framework with TypeScript + Tailwind
2. **Generate Landing Page**: From your copy and brand guidelines
3. **Add Analytics**: Google Analytics, Plausible, etc.
4. **Build for Production**: Optimized bundle
5. **Deploy to Vercel**: One-command deployment
6. **Custom Domain**: Automatic DNS configuration

### Usage Example

```python
from app.tools.website_launcher import WebsiteLauncher

launcher = WebsiteLauncher(workspace_root="./data/workspace")

# Complete workflow
result = launcher.full_launch_workflow(
    project_name="my-saas",
    copy={
        "hero_headline": "Ship Your SaaS in Days, Not Months",
        "hero_subheadline": "AI-powered business automation for founders",
        "cta_text": "Start Free Trial",
        "features": [
            {"title": "Automated Setup", "description": "..."},
            {"title": "Smart Agents", "description": "..."},
            {"title": "One-Click Deploy", "description": "..."},
        ]
    },
    brand={
        "colors": {"primary": "#3B82F6", "secondary": "#10B981"}
    },
    domain="mysaas.com",
    analytics_id="G-XXXXXXXXXX"
)

print(f"Live at: {result['url']}")
```

### Why Next.js + Vercel?

- **Maximum Automation**: Code-based = fully automatable
- **Fast Deployment**: 30 seconds from push to live
- **Zero Config**: Works out of the box
- **Scalable**: Handles traffic spikes automatically
- **SEO Friendly**: Server-side rendering built-in

### Alternative: Webflow/Framer

For no-code platforms, use the Playwright tool to:
- Create pages
- Add sections
- Configure settings
- Publish site

---

## Upgrade 4: Email Platform Integration

**Purpose**: Automate email marketing setup (sequences, forms, campaigns)

### Supported Providers

- **ConvertKit**: Creator-focused, great for courses/digital products
- **MailerLite**: Budget-friendly, good for small businesses
- **SMTP**: Fallback for transactional emails

### Automatable Tasks

- Create tags/segments
- Add subscribers
- Create opt-in forms
- Upload email sequences (20+ emails)
- Create and send broadcasts
- Test deliverability
- Get analytics

### Usage Example

```python
from app.tools.email_tool import EmailTool

tool = EmailTool(provider="convertkit", api_key="your_api_key")

# Create tag
tag = tool.create_tag("Free Trial Users")

# Add subscriber
tool.add_subscriber(
    email="user@example.com",
    first_name="Jane",
    tags=["Free Trial Users"]
)

# Create form
form = tool.create_form(
    name="Landing Page Signup",
    success_message="Check your email for confirmation!"
)

# Upload email sequence
emails = [
    {"subject": "Welcome!", "content": "...", "delay_days": 0},
    {"subject": "Getting Started", "content": "...", "delay_days": 1},
    {"subject": "Pro Tips", "content": "...", "delay_days": 3},
    # ... 17 more emails
]

tool.upload_email_sequence("Onboarding Sequence", emails)

# Test deliverability
tool.test_deliverability("your-email@example.com")
```

### Email Sequence Best Practices

**Onboarding Sequence (20 emails over 60 days)**:
- Days 0-7: Welcome, quick wins, feature education
- Days 8-30: Use cases, success stories, engagement
- Days 31-60: Advanced features, community, retention

---

## Upgrade 5: Marketing Operations Tool

**Purpose**: Generate and schedule months of content in minutes

### Content Generation

- **LinkedIn Posts**: 30-60 posts with hooks, insights, CTAs
- **Twitter Threads**: 10+ threads with 5-7 tweets each
- **Blog Articles**: Long-form SEO-optimized content
- **Email Newsletters**: Weekly/monthly newsletters
- **Instagram Captions**: Visual content copy

### Content Repurposing

Turn one piece of content into many:
- Blog article → 5 LinkedIn posts + 3 Twitter threads
- Video → Blog post + social snippets
- Podcast → Article + quotes + audiograms

### Content Calendar

- Generate 60-90 day calendars
- Schedule posts across platforms
- Track what's published
- Identify top performers
- Generate variants for A/B testing

### Usage Example

```python
from app.tools.marketing_ops_tool import MarketingOpsTool

tool = MarketingOpsTool(
    openai_api_key="...",
    openai_api_base="http://localhost:8000/v1",
    openai_model="Qwen/Qwen2.5-7B-Instruct",
    workspace_path="./data/marketing"
)

# Generate 30 LinkedIn posts
posts = tool.generate_linkedin_posts(
    topic="AI automation for small businesses",
    count=30,
    tone="professional",
    include_hooks=True
)

# Generate blog articles
articles = tool.generate_blog_articles(
    topics=[
        "How to Automate Your Business with AI",
        "10 Tasks Every Founder Should Automate",
        "Building a SaaS with AI Agents"
    ],
    word_count=1500,
    seo_optimized=True
)

# Repurpose article into social content
repurposed = tool.repurpose_content(
    source_content=articles["articles"][0]["content"],
    target_format="linkedin",
    source_format="article"
)

# Create content calendar
calendar = tool.create_content_calendar(
    start_date=datetime.now(),
    duration_days=60,
    posts_per_week=5,
    platforms=["linkedin", "twitter"]
)

# Assign content to calendar
tool.assign_content_to_calendar(
    calendar_file=calendar["file"],
    content_file=posts["file"]
)
```

### Time Savings

- **Manual**: 2-3 hours per week for content
- **With Tool**: 30 minutes per month for review/approval

---

## Upgrade 6: Paperwork Automation Agent

**Purpose**: Generate legal documents and pre-fill forms (90% done, you review and sign)

### Document Generation

- **Operating Agreement**: LLC formation document
- **Privacy Policy**: GDPR/CCPA compliant
- **Terms of Service**: Protect your business
- **Refund Policy**: Clear customer expectations
- **Service Agreements**: Client contracts
- **Business Plan**: Investor-ready outline

### Form Pre-filling

- LLC formation documents
- EIN application (IRS Form SS-4)
- State tax registration
- Business license applications

### Usage Example

```python
from app.agents.paperwork_agent import PaperworkAgent

agent = PaperworkAgent(
    openai_api_key="...",
    openai_api_base="http://localhost:8000/v1",
    openai_model="Qwen/Qwen2.5-7B-Instruct"
)

# Generate complete legal package
result = agent.generate_startup_legal_package(
    business_info={
        "name": "Acme SaaS Inc.",
        "state": "Delaware",
        "business_type": "LLC",
        "members": ["John Doe", "Jane Smith"],
        "website": "https://acmesaas.com",
        "services": "Project management software",
        "data_collected": ["email", "name", "usage data"],
        "third_party": ["Stripe", "Google Analytics"],
        "pricing_model": "subscription",
        "refund_policy": "30-day money-back guarantee"
    },
    output_dir="./data/legal_docs"
)

# Documents generated:
# - operating_agreement.md
# - privacy_policy.md
# - terms_of_service.md
# - refund_policy.md
# - tax_checklist.md
# - README.md (summary and next steps)
```

### Important Disclaimers

⚠️ **These are template documents for informational purposes only.**

- NOT legal advice
- NOT a substitute for an attorney
- State laws vary significantly
- Review and customize for your situation
- Have an attorney review before use

### The Reality of "Paperwork Filed"

**What the agent CAN do**:
- Generate document drafts (90% complete)
- Pre-fill forms with your information
- Provide filing instructions
- List required fees
- Link to filing websites

**What requires YOU**:
- Identity verification
- Human attestation/signature
- Sometimes notarization
- Payment submission
- Final review and approval

**Time Savings**: 5-10 hours of research and drafting → 10-15 minutes of review

---

## Updated Dependencies

Add to `backend/pyproject.toml`:

```toml
[project]
dependencies = [
    # ... existing dependencies
    "playwright>=1.40.0",
    "google-cloud-compute>=1.15.0",
    "google-cloud-run>=0.10.0",
    "google-cloud-secret-manager>=2.16.0",
]
```

Install Playwright browsers:

```bash
playwright install chromium
```

---

## Configuration Updates

Add to `backend/.env`:

```env
# Browser Automation
PLAYWRIGHT_HEADLESS=true
PLAYWRIGHT_TIMEOUT=30000

# Google Cloud
GCLOUD_PROJECT_ID=your-project-id
GCLOUD_MODE=cli  # or "api"
GCLOUD_CREDENTIALS_PATH=/path/to/credentials.json  # for API mode

# Email Marketing
EMAIL_PROVIDER=convertkit  # or mailerlite
CONVERTKIT_API_KEY=your_api_key
MAILERLITE_API_KEY=your_api_key

# Website Deployment
VERCEL_TOKEN=your_vercel_token

# Marketing Content
MARKETING_WORKSPACE=./data/marketing
```

---

## Agent Permission Updates

Updated permissions in `backend/app/core/permissions.py`:

```python
AGENT_PERMISSIONS = {
    "orchestrator": {
        "filesystem", "shell", "git", "gcloud"
    },
    "business_builder": {
        "filesystem", "marketing_ops"
    },
    "webdev": {
        "filesystem", "shell", "git", "playwright", "website_launcher", "gcloud"
    },
    "stripe_agent": {
        "filesystem", "stripe", "playwright"
    },
    "marketing": {
        "filesystem", "playwright", "email", "social", "marketing_ops"
    },
    "paperwork": {
        "filesystem"
    },
    "reviewer": {
        "filesystem"
    },
}
```

---

## Example: Complete Business Launch

Here's how all upgrades work together:

```python
# 1. Generate business documents
paperwork_agent.generate_startup_legal_package(business_info, "./legal")

# 2. Set up cloud infrastructure
gcloud_tool.create_project("my-saas")
gcloud_tool.enable_common_apis("my-saas")

# 3. Launch website
website_launcher.full_launch_workflow(
    project_name="my-saas",
    copy=copy_data,
    brand=brand_data,
    domain="mysaas.com"
)

# 4. Set up payments (with browser automation for dashboard tasks)
playwright_tool.navigate("https://dashboard.stripe.com")
# ... automate product creation

# 5. Set up email marketing
email_tool.create_form("Landing Page Signup")
email_tool.upload_email_sequence("Onboarding", onboarding_emails)

# 6. Generate 60 days of content
marketing_tool.generate_linkedin_posts(topic="...", count=30)
marketing_tool.create_content_calendar(duration_days=60)

# Total time: 2-3 hours (vs. 2-3 weeks manually)
```

---

## Next Steps

1. **Install new dependencies**: `pip install -e backend/`
2. **Configure environment**: Update `.env` with API keys
3. **Test each upgrade**: Run example scripts
4. **Review permissions**: Ensure agents have appropriate access
5. **Customize for your use case**: Modify prompts and workflows

---

## Support

For questions or issues with the upgrades:
- Check the main README.md
- Review ARCHITECTURE.md for technical details
- Open an issue on GitHub
- Consult the API documentation at `/docs`

---

**Remember**: These tools automate the tedious 90%, but you're still the founder. Review everything, make strategic decisions, and maintain human oversight for critical operations.
