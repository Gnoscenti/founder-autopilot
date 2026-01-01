# Quick Start Guide

Get Founder Autopilot running in 10 minutes.

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- 8GB RAM minimum

---

## Step 1: Clone Repository

```bash
git clone https://github.com/Gnoscenti/founder-autopilot.git
cd founder-autopilot
```

---

## Step 2: Set Up vLLM (Local Model)

**Option A: Use vLLM (Recommended for development)**

```bash
# Install vLLM
pip install vllm

# Start model server (in a separate terminal)
vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --port 8000

# Keep this running in the background
```

**Option B: Use OpenAI API**

Skip vLLM setup and use your OpenAI API key in Step 4.

---

## Step 3: Set Up Backend

```bash
cd backend

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install chromium

# Create data directories
mkdir -p data/workspace data/artifacts data/browser_sessions
```

---

## Step 4: Configure Environment

Create `backend/.env`:

```bash
# Copy example
cp .env.example .env

# Edit .env
nano .env
```

**For vLLM (local model):**

```env
# OpenAI / vLLM Configuration
OPENAI_API_KEY=EMPTY
OPENAI_API_BASE=http://localhost:8000/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct

# Optional: Add API keys for integrations
STRIPE_API_KEY=sk_test_...
CONVERTKIT_API_KEY=...
VERCEL_TOKEN=...
```

**For OpenAI API:**

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4-turbo-preview
```

---

## Step 5: Start Backend

```bash
cd backend
python -m app.main
```

Backend will start at `http://localhost:8001`

Visit `http://localhost:8001/docs` for API documentation.

---

## Step 6: Set Up Frontend

**In a new terminal:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at `http://localhost:3000`

---

## Step 7: Test the System

Open `http://localhost:3000` in your browser.

### Quick Test: Generate Business Concepts

1. Go to **Business Spec** page
2. Fill in your constraints:
   - Skills: "Software development, marketing"
   - Time: "10 hours/week"
   - Budget: "$500"
   - Target income: "$5000/month"
3. Click **Save Spec**

4. Go to **Prompt Library**
5. Find "Generate 3 Business Concepts"
6. Click **Use Prompt**

7. Go to **Launch Run**
8. Enter goal: "Generate 3 business concepts based on my spec"
9. Click **Launch Run**
10. Watch the orchestrator create and execute tasks

---

## Step 8: Optional Integrations

### Google Cloud CLI

```bash
# Install gcloud
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login
gcloud auth login

# Set project
gcloud config set project your-project-id
```

### Vercel CLI

```bash
# Install
npm install -g vercel

# Login
vercel login
```

### Stripe

1. Create account at https://stripe.com
2. Get API key from Dashboard → Developers → API keys
3. Add to `.env`: `STRIPE_API_KEY=sk_test_...`

### Email Marketing (ConvertKit or MailerLite)

1. Create account
2. Get API key from settings
3. Add to `.env`: `CONVERTKIT_API_KEY=...`

---

## Usage Examples

### Example 1: Generate Legal Documents

```bash
# Using curl
curl -X POST http://localhost:8001/api/paperwork/legal-package \
  -H "Content-Type: application/json" \
  -d '{
    "business_info": {
      "name": "My SaaS LLC",
      "state": "Delaware",
      "business_type": "LLC"
    }
  }'
```

### Example 2: Generate Marketing Content

```bash
curl -X POST http://localhost:8001/api/marketing/linkedin-posts \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI automation for small businesses",
    "count": 10,
    "tone": "professional"
  }'
```

### Example 3: Launch Website

```bash
curl -X POST http://localhost:8001/api/website/launch \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "my-saas",
    "copy": {
      "hero_headline": "Ship Your SaaS Faster",
      "hero_subheadline": "AI-powered tools for founders"
    },
    "brand": {
      "colors": {"primary": "#3B82F6"}
    }
  }'
```

---

## Troubleshooting

### Backend won't start

```bash
# Check if port 8001 is in use
lsof -i :8001

# Kill process if needed
kill -9 <PID>

# Try different port
API_PORT=8002 python -m app.main
```

### Frontend won't start

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Try different port
PORT=3001 npm run dev
```

### vLLM model not loading

```bash
# Check available memory
free -h

# Use smaller model if needed
vllm serve Qwen/Qwen2.5-3B-Instruct --dtype auto --port 8000

# Or use quantized model
vllm serve TheBloke/Mistral-7B-Instruct-v0.2-GPTQ --dtype auto --port 8000
```

### Playwright browser errors

```bash
# Reinstall browsers
playwright install --force chromium

# Run in headed mode for debugging
PLAYWRIGHT_HEADLESS=false python -m app.main
```

---

## Next Steps

1. **Read the docs**:
   - [README.md](README.md) - Full documentation
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [UPGRADES.md](UPGRADES.md) - Feature details
   - [EXAMPLES.md](EXAMPLES.md) - Usage examples

2. **Try the examples**:
   - Start with Example 1 in EXAMPLES.md
   - Launch a complete SaaS in one day

3. **Customize**:
   - Edit prompts in `backend/app/prompts/business_prompts.json`
   - Add your own agents in `backend/app/agents/`
   - Create custom tools in `backend/app/tools/`

4. **Deploy**:
   - Backend: Railway, Render, Fly.io
   - Frontend: Vercel, Netlify, Cloudflare Pages

---

## Common Commands

```bash
# Start vLLM
vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --port 8000

# Start backend
cd backend && python -m app.main

# Start frontend
cd frontend && npm run dev

# Run tests
cd backend && pytest

# Format code
cd backend && black . && ruff check .

# Build frontend
cd frontend && npm run build

# View logs
tail -f backend/data/runs.db
```

---

## Support

- **Issues**: https://github.com/Gnoscenti/founder-autopilot/issues
- **Discussions**: https://github.com/Gnoscenti/founder-autopilot/discussions
- **Documentation**: https://github.com/Gnoscenti/founder-autopilot

---

**You're ready to automate your business launch! 🚀**
