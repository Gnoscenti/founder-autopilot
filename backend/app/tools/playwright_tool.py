"""Playwright tool - browser automation for tasks without APIs."""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page


class PlaywrightTool:
    """Tool for browser automation using Playwright with session persistence."""
    
    # Allowlisted domains for security
    ALLOWED_DOMAINS = [
        "stripe.com",
        "dashboard.stripe.com",
        "webflow.com",
        "framer.com",
        "namecheap.com",
        "godaddy.com",
        "cloudflare.com",
        "vercel.com",
        "netlify.com",
        "convertkit.com",
        "mailerlite.com",
        "linkedin.com",
        "twitter.com",
        "facebook.com",
    ]
    
    def __init__(self, session_dir: str = "./data/browser_sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}
        self.pages: Dict[str, Page] = {}
    
    async def initialize(self, headless: bool = True):
        """Initialize browser with persistent session support."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=headless,
                args=['--disable-blink-features=AutomationControlled']
            )
    
    def _is_domain_allowed(self, url: str) -> bool:
        """Check if domain is in allowlist."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        # Check if domain or parent domain is allowed
        for allowed in self.ALLOWED_DOMAINS:
            if domain == allowed or domain.endswith(f".{allowed}"):
                return True
        
        return False
    
    def _get_session_path(self, session_name: str) -> Path:
        """Get path to session storage."""
        return self.session_dir / f"{session_name}_state.json"
    
    async def create_context(
        self,
        session_name: str = "default",
        load_session: bool = True
    ) -> BrowserContext:
        """Create or restore browser context with session persistence."""
        if not self.browser:
            await self.initialize()
        
        session_path = self._get_session_path(session_name)
        
        # Load existing session if available
        storage_state = None
        if load_session and session_path.exists():
            try:
                with open(session_path) as f:
                    storage_state = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load session: {e}")
        
        # Create context
        context = await self.browser.new_context(
            storage_state=storage_state,
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        self.contexts[session_name] = context
        return context
    
    async def save_session(self, session_name: str = "default"):
        """Save browser session state (cookies, localStorage, etc.)."""
        if session_name not in self.contexts:
            return {"success": False, "error": "Context not found"}
        
        context = self.contexts[session_name]
        session_path = self._get_session_path(session_name)
        
        try:
            storage_state = await context.storage_state()
            with open(session_path, 'w') as f:
                json.dump(storage_state, f, indent=2)
            
            return {"success": True, "path": str(session_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def navigate(
        self,
        url: str,
        session_name: str = "default",
        wait_until: str = "networkidle"
    ) -> Dict[str, Any]:
        """Navigate to URL with domain validation."""
        
        # Security check
        if not self._is_domain_allowed(url):
            return {
                "success": False,
                "error": f"Domain not allowed. Allowlisted domains: {', '.join(self.ALLOWED_DOMAINS)}"
            }
        
        try:
            # Get or create context
            if session_name not in self.contexts:
                await self.create_context(session_name)
            
            context = self.contexts[session_name]
            
            # Create new page or reuse existing
            if session_name not in self.pages:
                self.pages[session_name] = await context.new_page()
            
            page = self.pages[session_name]
            
            # Navigate
            response = await page.goto(url, wait_until=wait_until, timeout=30000)
            
            return {
                "success": True,
                "url": page.url,
                "title": await page.title(),
                "status": response.status if response else None
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def click(
        self,
        selector: str,
        session_name: str = "default",
        wait_for_navigation: bool = False
    ) -> Dict[str, Any]:
        """Click element by selector."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            
            # Wait for element
            await page.wait_for_selector(selector, timeout=10000)
            
            # Click
            if wait_for_navigation:
                async with page.expect_navigation():
                    await page.click(selector)
            else:
                await page.click(selector)
            
            return {"success": True, "url": page.url}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def fill(
        self,
        selector: str,
        value: str,
        session_name: str = "default"
    ) -> Dict[str, Any]:
        """Fill form field."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            await page.wait_for_selector(selector, timeout=10000)
            await page.fill(selector, value)
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def select(
        self,
        selector: str,
        value: str,
        session_name: str = "default"
    ) -> Dict[str, Any]:
        """Select dropdown option."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            await page.wait_for_selector(selector, timeout=10000)
            await page.select_option(selector, value)
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_text(
        self,
        selector: str,
        session_name: str = "default"
    ) -> Dict[str, Any]:
        """Extract text from element."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            await page.wait_for_selector(selector, timeout=10000)
            text = await page.text_content(selector)
            
            return {"success": True, "text": text}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def screenshot(
        self,
        path: str,
        session_name: str = "default",
        full_page: bool = False
    ) -> Dict[str, Any]:
        """Take screenshot."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            await page.screenshot(path=path, full_page=full_page)
            
            return {"success": True, "path": path}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def wait_for_selector(
        self,
        selector: str,
        session_name: str = "default",
        timeout: int = 10000
    ) -> Dict[str, Any]:
        """Wait for element to appear."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            await page.wait_for_selector(selector, timeout=timeout)
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def evaluate(
        self,
        script: str,
        session_name: str = "default"
    ) -> Dict[str, Any]:
        """Execute JavaScript in page context."""
        if session_name not in self.pages:
            return {"success": False, "error": "No active page"}
        
        try:
            page = self.pages[session_name]
            result = await page.evaluate(script)
            
            return {"success": True, "result": result}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def close_context(self, session_name: str = "default"):
        """Close browser context and save session."""
        if session_name in self.contexts:
            await self.save_session(session_name)
            await self.contexts[session_name].close()
            del self.contexts[session_name]
            
            if session_name in self.pages:
                del self.pages[session_name]
    
    async def close(self):
        """Close all contexts and browser."""
        # Save all sessions
        for session_name in list(self.contexts.keys()):
            await self.close_context(session_name)
        
        # Close browser
        if self.browser:
            await self.browser.close()
        
        # Stop playwright
        if self.playwright:
            await self.playwright.stop()


# Synchronous wrapper for easier use
class PlaywrightToolSync:
    """Synchronous wrapper for PlaywrightTool."""
    
    def __init__(self, session_dir: str = "./data/browser_sessions"):
        self.tool = PlaywrightTool(session_dir)
        self.loop = None
    
    def _run_async(self, coro):
        """Run async function in event loop."""
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        return self.loop.run_until_complete(coro)
    
    def navigate(self, url: str, session_name: str = "default") -> Dict[str, Any]:
        return self._run_async(self.tool.navigate(url, session_name))
    
    def click(self, selector: str, session_name: str = "default") -> Dict[str, Any]:
        return self._run_async(self.tool.click(selector, session_name))
    
    def fill(self, selector: str, value: str, session_name: str = "default") -> Dict[str, Any]:
        return self._run_async(self.tool.fill(selector, value, session_name))
    
    def save_session(self, session_name: str = "default") -> Dict[str, Any]:
        return self._run_async(self.tool.save_session(session_name))
    
    def close(self):
        self._run_async(self.tool.close())
        if self.loop:
            self.loop.close()
