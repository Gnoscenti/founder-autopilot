# Founder Autopilot - Usage Examples

Real-world examples showing how to use the upgraded Founder Autopilot system to launch a business.

---

## Example 1: Launch a SaaS in One Day

**Goal**: Launch a project management SaaS from concept to live website with payments and email marketing.

### Step 1: Generate Business Documents (15 minutes)

```python
from app.agents.paperwork_agent import PaperworkAgent

agent = PaperworkAgent(
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:8000/v1",
    openai_model="Qwen/Qwen2.5-7B-Instruct"
)

result = agent.generate_startup_legal_package(
    business_info={
        "name": "TaskFlow Pro LLC",
        "state": "Delaware",
        "business_type": "LLC",
        "members": ["John Founder"],
        "website": "https://taskflowpro.com",
        "services": "Project management software for remote teams",
        "data_collected": ["email", "name", "project data", "usage analytics"],
        "third_party": ["Stripe", "Google Analytics", "AWS"],
        "pricing_model": "subscription",
        "refund_policy": "30-day money-back guarantee"
    },
    output_dir="./data/legal_docs/taskflow"
)

# Output:
# - operating_agreement.md
# - privacy_policy.md
# - terms_of_service.md
# - refund_policy.md
# - tax_checklist.md
```

**Time saved**: 8-12 hours of research and drafting

### Step 2: Set Up Cloud Infrastructure (10 minutes)

```python
from app.tools.gcloud_tool import GCloudTool

gcloud = GCloudTool(mode="cli")

# Create project
gcloud.create_project("taskflow-prod", "TaskFlow Production")
gcloud.set_project("taskflow-prod")

# Enable APIs
gcloud.enable_common_apis("taskflow-prod")

# Create service account for backend
gcloud.create_service_account(
    "backend-api",
    "Backend API Service Account",
    project_id="taskflow-prod"
)

# Create secrets
gcloud.create_secret("stripe-api-key", project_id="taskflow-prod")
gcloud.add_secret_version("stripe-api-key", "sk_live_...", project_id="taskflow-prod")

gcloud.create_secret("database-url", project_id="taskflow-prod")
gcloud.add_secret_version("database-url", "postgresql://...", project_id="taskflow-prod")
```

**Time saved**: 2-3 hours of manual setup and documentation reading

### Step 3: Launch Marketing Website (30 minutes)

```python
from app.tools.website_launcher import WebsiteLauncher

launcher = WebsiteLauncher(workspace_root="./data/workspace")

result = launcher.full_launch_workflow(
    project_name="taskflow-website",
    copy={
        "hero_headline": "Project Management That Actually Works",
        "hero_subheadline": "Built for remote teams who need clarity, not complexity. Get everyone on the same page in minutes.",
        "cta_text": "Start Free 14-Day Trial",
        "features": [
            {
                "title": "Visual Task Boards",
                "description": "Drag-and-drop simplicity meets powerful automation"
            },
            {
                "title": "Real-Time Collaboration",
                "description": "Comments, mentions, and notifications that keep everyone in sync"
            },
            {
                "title": "Smart Insights",
                "description": "AI-powered analytics show what's working and what needs attention"
            }
        ]
    },
    brand={
        "colors": {
            "primary": "#6366F1",
            "secondary": "#10B981"
        }
    },
    domain="taskflowpro.com",
    analytics_id="G-XXXXXXXXXX"
)

print(f"Website live at: {result['url']}")
```

**Time saved**: 2-3 days of design, development, and deployment

### Step 4: Set Up Stripe Products (20 minutes)

```python
from app.tools.playwright_tool import PlaywrightToolSync

browser = PlaywrightToolSync()

# Navigate to Stripe dashboard (you login once)
browser.navigate("https://dashboard.stripe.com/products", session_name="stripe")

# Create Starter plan
browser.click("button[data-test='create-product']")
browser.fill("input[name='name']", "Starter Plan")
browser.fill("textarea[name='description']", "Perfect for small teams (up to 10 users)")
browser.click("button[type='submit']")

# Add pricing
browser.click("button[data-test='add-price']")
browser.fill("input[name='unit_amount']", "2900")  # $29.00
browser.select("select[name='recurring']", "month")
browser.click("button[type='submit']")

# Create Pro plan
browser.click("button[data-test='create-product']")
browser.fill("input[name='name']", "Pro Plan")
browser.fill("textarea[name='description']", "For growing teams (up to 50 users)")
browser.fill("input[name='unit_amount']", "9900")  # $99.00
browser.click("button[type='submit']")

# Save session for future use
browser.save_session("stripe")
browser.close()
```

**Time saved**: Manual clicking replaced with automation

### Step 5: Set Up Email Marketing (25 minutes)

```python
from app.tools.email_tool import EmailTool

email = EmailTool(provider="convertkit", api_key="your_api_key")

# Create tags
email.create_tag("Free Trial")
email.create_tag("Starter Plan")
email.create_tag("Pro Plan")

# Create signup form
form = email.create_form(
    name="Landing Page Signup",
    success_message="Check your email! Your free trial is ready."
)

# Upload onboarding sequence
onboarding_emails = [
    {
        "subject": "Welcome to TaskFlow Pro! 🎉",
        "content": "Hi there! I'm excited to help you get started...",
        "delay_days": 0
    },
    {
        "subject": "Quick Win: Create Your First Project",
        "content": "Let's get your first project set up in 5 minutes...",
        "delay_days": 1
    },
    {
        "subject": "Pro Tip: Automate Your Workflows",
        "content": "Did you know you can automate repetitive tasks?...",
        "delay_days": 3
    },
    # ... 17 more emails covering features, use cases, success stories
]

email.upload_email_sequence("Onboarding Sequence", onboarding_emails)

# Test deliverability
email.test_deliverability("john@taskflowpro.com")
```

**Time saved**: 4-6 hours of email writing and platform setup

### Step 6: Generate Launch Content (45 minutes)

```python
from app.tools.marketing_ops_tool import MarketingOpsTool
from datetime import datetime

marketing = MarketingOpsTool(
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:8000/v1",
    openai_model="Qwen/Qwen2.5-7B-Instruct",
    workspace_path="./data/marketing/taskflow"
)

# Generate 30 LinkedIn posts
linkedin = marketing.generate_linkedin_posts(
    topic="Project management for remote teams",
    count=30,
    tone="professional",
    include_hooks=True
)

# Generate Twitter threads
twitter = marketing.generate_twitter_threads(
    topic="Remote team productivity tips",
    count=10,
    tweets_per_thread=7
)

# Generate blog articles
articles = marketing.generate_blog_articles(
    topics=[
        "10 Project Management Mistakes Remote Teams Make",
        "How to Run Effective Async Standups",
        "The Ultimate Guide to Remote Team Collaboration"
    ],
    word_count=1500,
    seo_optimized=True
)

# Create 60-day content calendar
calendar = marketing.create_content_calendar(
    start_date=datetime.now(),
    duration_days=60,
    posts_per_week=5,
    platforms=["linkedin", "twitter"]
)

# Assign content to calendar
marketing.assign_content_to_calendar(
    calendar_file=calendar["file"],
    content_file=linkedin["file"]
)

print(f"Generated {linkedin['count']} LinkedIn posts")
print(f"Generated {twitter['count']} Twitter threads")
print(f"Generated {len(articles['articles'])} blog articles")
print(f"Content calendar: {calendar['total_posts']} posts scheduled")
```

**Time saved**: 20-30 hours of content creation

### Total Time: ~2.5 hours (vs. 2-3 weeks manually)

---

## Example 2: Repurpose Content at Scale

**Goal**: Turn one blog article into 20+ pieces of content across platforms.

```python
from app.tools.marketing_ops_tool import MarketingOpsTool

marketing = MarketingOpsTool(...)

# Original article (1500 words)
article = """
# How to Build a Remote-First Company Culture

Remote work is here to stay, but many companies struggle with culture...
[full article content]
"""

# Repurpose into LinkedIn posts
linkedin = marketing.repurpose_content(
    source_content=article,
    target_format="linkedin",
    source_format="article"
)
# Output: 5 LinkedIn posts

# Repurpose into Twitter threads
twitter = marketing.repurpose_content(
    source_content=article,
    target_format="twitter",
    source_format="article"
)
# Output: 3 Twitter threads (5-7 tweets each)

# Repurpose into email newsletter
newsletter = marketing.repurpose_content(
    source_content=article,
    target_format="email",
    source_format="article"
)
# Output: 1 email newsletter

# Repurpose into Instagram captions
instagram = marketing.repurpose_content(
    source_content=article,
    target_format="instagram",
    source_format="article"
)
# Output: 10 Instagram captions

# Repurpose into short video scripts
videos = marketing.repurpose_content(
    source_content=article,
    target_format="short_video",
    source_format="article"
)
# Output: 5 video scripts (60-90 seconds each)

# Total: 1 article → 24 pieces of content
```

**Time saved**: 8-10 hours of manual repurposing

---

## Example 3: A/B Test Content Performance

**Goal**: Find what resonates with your audience by testing variants.

```python
from app.tools.marketing_ops_tool import MarketingOpsTool

marketing = MarketingOpsTool(...)

# Original high-performing post
original = """
Remote work isn't the problem.

Bad management is.

Here's what great remote leaders do differently:

1. They over-communicate
2. They document everything
3. They trust their team
4. They measure outcomes, not hours
5. They invest in tools

The result? Teams that are more productive AND happier.

What would you add to this list?
"""

# Generate 5 variants to test
variants = marketing.generate_content_variants(
    original_post=original,
    count=5
)

# Variants will test:
# - Different hooks ("Remote work isn't the problem" vs "Your team isn't lazy")
# - Different structures (list vs story vs question)
# - Different CTAs ("What would you add?" vs "Share this with your team")

# Post variants on different days and track engagement
# Use top performer as template for future content
```

---

## Example 4: Automate Weekly Content Routine

**Goal**: Spend 30 minutes on Monday, have content for the entire week.

```python
from app.tools.marketing_ops_tool import MarketingOpsTool
from datetime import datetime, timedelta

marketing = MarketingOpsTool(...)

# Monday morning routine
def weekly_content_routine():
    # 1. Generate this week's LinkedIn posts (5 posts)
    linkedin = marketing.generate_linkedin_posts(
        topic="Remote team management tips",
        count=5,
        tone="professional"
    )
    
    # 2. Generate Twitter threads (2 threads)
    twitter = marketing.generate_twitter_threads(
        topic="Productivity hacks for remote workers",
        count=2,
        tweets_per_thread=5
    )
    
    # 3. Create calendar for this week
    calendar = marketing.create_content_calendar(
        start_date=datetime.now(),
        duration_days=7,
        posts_per_week=5,
        platforms=["linkedin", "twitter"]
    )
    
    # 4. Assign content to calendar
    marketing.assign_content_to_calendar(
        calendar_file=calendar["file"],
        content_file=linkedin["file"]
    )
    
    # 5. Review and schedule in your social media tool
    # (Buffer, Hootsuite, etc.)
    
    return {
        "linkedin_posts": linkedin["count"],
        "twitter_threads": twitter["count"],
        "calendar": calendar["file"]
    }

# Run every Monday
result = weekly_content_routine()
print(f"Week prepared: {result['linkedin_posts']} posts, {result['twitter_threads']} threads")
```

**Time saved**: 2-3 hours per week → 30 minutes per week

---

## Example 5: Complete Business Formation

**Goal**: File LLC, get EIN, set up bank account, file taxes.

```python
from app.agents.paperwork_agent import PaperworkAgent
from app.tools.gcloud_tool import GCloudTool

paperwork = PaperworkAgent(...)

# Step 1: Generate formation documents
llc_docs = paperwork.pre_fill_llc_formation(
    business_info={
        "name": "TaskFlow Pro LLC",
        "state": "Delaware",
        "registered_agent": "John Founder",
        "address": "123 Main St, Wilmington, DE 19801",
        "members": [
            {"name": "John Founder", "ownership": 100}
        ],
        "management": "member-managed"
    },
    state="Delaware"
)

# Step 2: Review and file (HUMAN REQUIRED)
# - Visit Delaware Division of Corporations website
# - Upload pre-filled documents
# - Pay filing fee ($90)
# - Wait 1-2 business days for approval

# Step 3: Apply for EIN (HUMAN REQUIRED)
# - Visit IRS.gov
# - Use pre-filled SS-4 information
# - Complete online application
# - Receive EIN immediately

# Step 4: Generate tax checklist
tax_checklist = paperwork.generate_tax_checklist(
    business_type="LLC",
    state="Delaware"
)

# Step 5: Set up accounting (optional automation)
# - QuickBooks/Xero integration
# - Connect bank account
# - Set up expense tracking

print("Formation documents ready for review and filing")
print(f"Next steps: {llc_docs['next_steps']}")
```

**Time saved**: 10-15 hours of research and form-filling

---

## Example 6: Deploy Backend API to Cloud Run

**Goal**: Deploy FastAPI backend with database and secrets.

```python
from app.tools.gcloud_tool import GCloudTool

gcloud = GCloudTool(mode="cli")

# 1. Build container
import subprocess
subprocess.run([
    "docker", "build",
    "-t", "gcr.io/taskflow-prod/api:latest",
    "./backend"
])

# 2. Push to Google Container Registry
subprocess.run([
    "docker", "push",
    "gcr.io/taskflow-prod/api:latest"
])

# 3. Deploy to Cloud Run
result = gcloud.deploy_cloud_run(
    service_name="taskflow-api",
    image="gcr.io/taskflow-prod/api:latest",
    region="us-central1",
    allow_unauthenticated=True,
    env_vars={
        "DATABASE_URL": "secret:database-url",  # Reference to secret
        "STRIPE_API_KEY": "secret:stripe-api-key",
        "OPENAI_API_KEY": "secret:openai-api-key"
    },
    project_id="taskflow-prod"
)

# 4. Get deployment URL
url_result = gcloud.get_cloud_run_url("taskflow-api", region="us-central1")
print(f"API deployed at: {url_result['url']}")

# 5. Update frontend environment variables
# NEXT_PUBLIC_API_URL=https://taskflow-api-xxx.run.app
```

**Time saved**: 2-4 hours of deployment configuration

---

## Example 7: Browser Automation for No-API Services

**Goal**: Automate tasks on platforms without APIs.

```python
from app.tools.playwright_tool import PlaywrightToolSync

browser = PlaywrightToolSync()

# Example 1: Set up Webflow site
browser.navigate("https://webflow.com/dashboard", session_name="webflow")
# (you login once)

browser.click("button[data-test='create-site']")
browser.fill("input[name='site-name']", "TaskFlow Marketing Site")
browser.select("select[name='template']", "saas-template")
browser.click("button[type='submit']")

# Example 2: Configure Cloudflare DNS
browser.navigate("https://dash.cloudflare.com", session_name="cloudflare")

browser.click("a[href*='taskflowpro.com']")
browser.click("button[data-test='add-record']")
browser.select("select[name='type']", "A")
browser.fill("input[name='name']", "@")
browser.fill("input[name='content']", "76.76.21.21")  # Vercel IP
browser.click("button[type='submit']")

# Example 3: Post to LinkedIn (with approval)
browser.navigate("https://linkedin.com", session_name="linkedin")

browser.click("button[aria-label='Start a post']")
browser.fill("div[role='textbox']", """
Remote work isn't the problem. Bad management is.

Here's what great remote leaders do differently:
[full post content]
""")

# HUMAN APPROVAL REQUIRED before posting
input("Review post and press Enter to publish...")
browser.click("button[data-test='share-action']")

browser.close()
```

---

## Best Practices

### 1. Always Review AI-Generated Content

```python
# Don't do this:
result = marketing.generate_linkedin_posts(...)
# immediately post without review

# Do this:
result = marketing.generate_linkedin_posts(...)
print(f"Generated {result['count']} posts")
print(f"Saved to: {result['file']}")
# Review file, edit as needed, then schedule
```

### 2. Use Human-in-the-Loop for Critical Operations

```python
# Operations requiring approval:
# - Git push to production
# - Stripe product creation
# - Email campaign sending
# - Social media posting
# - Legal document filing

# Pattern:
result = agent.generate_document(...)
print("Document generated. Please review:")
print(result['content'][:500])
approval = input("Approve? (yes/no): ")
if approval.lower() == "yes":
    agent.file_document(...)
```

### 3. Save Sessions for Reuse

```python
# Login once, reuse forever
browser.navigate("https://dashboard.stripe.com", session_name="stripe")
# ... do work
browser.save_session("stripe")

# Next time (no login required)
browser.navigate("https://dashboard.stripe.com", session_name="stripe")
# Session restored automatically
```

### 4. Use Version Control for Generated Content

```python
# Save all generated content to git
import subprocess

marketing.generate_linkedin_posts(...)
subprocess.run(["git", "add", "data/marketing/"])
subprocess.run(["git", "commit", "-m", "Generated weekly content"])
subprocess.run(["git", "push"])
```

---

## Troubleshooting

### Issue: vLLM model not loading

```bash
# Check if vLLM is running
curl http://localhost:8000/v1/models

# If not, start vLLM
vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --port 8000
```

### Issue: Playwright browser not found

```bash
# Install browsers
playwright install chromium
```

### Issue: gcloud command not found

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### Issue: Vercel deployment fails

```bash
# Login to Vercel
vercel login

# Link project
cd project-directory
vercel link
```

---

## Next Steps

1. **Try the examples**: Start with Example 1 (Launch a SaaS)
2. **Customize for your business**: Modify prompts and workflows
3. **Build your own workflows**: Combine tools in new ways
4. **Share your results**: Contribute examples back to the community

---

**Remember**: These tools are force multipliers, not replacements for founder judgment. Use them to automate the tedious 90%, then focus your energy on the strategic 10% that makes or breaks your business.
