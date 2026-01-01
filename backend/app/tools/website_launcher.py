"""Website Launcher tool - automate Next.js website creation and deployment."""
from typing import Dict, Any, Optional, List
from pathlib import Path
import subprocess
import json
import re


class WebsiteLauncher:
    """Tool for automated website generation and deployment."""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
    
    def _run_command(
        self,
        command: str,
        cwd: Optional[Path] = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Run shell command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.workspace_root,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout} seconds"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_nextjs_project(
        self,
        project_name: str,
        typescript: bool = True,
        tailwind: bool = True,
        app_router: bool = True
    ) -> Dict[str, Any]:
        """Create a new Next.js project."""
        
        project_path = self.workspace_root / project_name
        
        if project_path.exists():
            return {"success": False, "error": f"Project {project_name} already exists"}
        
        # Build create-next-app command
        flags = [
            '--yes',  # Skip prompts
            f'--{("typescript" if typescript else "javascript")}',
            f'--{"" if tailwind else "no-"}tailwind',
            f'--{"" if app_router else "no-"}app',
            '--no-src-dir',
            '--import-alias "@/*"',
        ]
        
        command = f'npx create-next-app@latest {project_name} {" ".join(flags)}'
        
        result = self._run_command(command, timeout=180)
        
        if result["success"]:
            result["project_path"] = str(project_path)
        
        return result
    
    def write_page_component(
        self,
        project_name: str,
        page_path: str,
        content: str,
        is_typescript: bool = True
    ) -> Dict[str, Any]:
        """Write a page component to the Next.js project."""
        
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        # Determine file extension
        ext = "tsx" if is_typescript else "jsx"
        
        # Write file
        file_path = project_path / "app" / f"{page_path}.{ext}"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            return {"success": True, "file_path": str(file_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_landing_page(
        self,
        project_name: str,
        copy: Dict[str, Any],
        brand: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a complete landing page from copy and brand."""
        
        # Extract copy sections
        hero_headline = copy.get("hero_headline", "Welcome")
        hero_subheadline = copy.get("hero_subheadline", "")
        cta_text = copy.get("cta_text", "Get Started")
        features = copy.get("features", [])
        
        # Extract brand
        colors = brand.get("colors", {})
        primary_color = colors.get("primary", "#3B82F6")
        
        # Generate Next.js component
        component = f'''export default function Home() {{
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            {hero_headline}
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            {hero_subheadline}
          </p>
          <button 
            className="px-8 py-4 text-lg font-semibold text-white rounded-lg transition-colors"
            style={{{{ backgroundColor: '{primary_color}' }}}}
          >
            {cta_text}
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {", ".join([f'{{"title": "{f.get("title", "")}", "description": "{f.get("description", "")}"}}' for f in features[:3]])}
          ].map((feature, i) => (
            <div key={{i}} className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-xl font-semibold mb-3">{{feature.title}}</h3>
              <p className="text-gray-600">{{feature.description}}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}}
'''
        
        return self.write_page_component(project_name, "page", component)
    
    def install_dependencies(self, project_name: str) -> Dict[str, Any]:
        """Install npm dependencies."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        return self._run_command("npm install", cwd=project_path, timeout=300)
    
    def build_project(self, project_name: str) -> Dict[str, Any]:
        """Build Next.js project for production."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        return self._run_command("npm run build", cwd=project_path, timeout=300)
    
    def deploy_to_vercel(
        self,
        project_name: str,
        production: bool = True,
        env_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Deploy project to Vercel."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        # Build command
        command = "vercel"
        if production:
            command += " --prod"
        else:
            command += " --yes"
        
        # Add environment variables
        if env_vars:
            for key, value in env_vars.items():
                command += f' -e {key}="{value}"'
        
        result = self._run_command(command, cwd=project_path, timeout=300)
        
        # Extract URL from output
        if result["success"]:
            # Look for deployment URL in output
            url_match = re.search(r'https://[^\s]+\.vercel\.app', result["stdout"])
            if url_match:
                result["url"] = url_match.group(0)
        
        return result
    
    def set_vercel_env(
        self,
        project_name: str,
        key: str,
        value: str,
        environment: str = "production"
    ) -> Dict[str, Any]:
        """Set environment variable in Vercel project."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        command = f'vercel env add {key} {environment} <<< "{value}"'
        return self._run_command(command, cwd=project_path)
    
    def link_vercel_project(
        self,
        project_name: str,
        vercel_project_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Link local project to Vercel project."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        command = "vercel link --yes"
        if vercel_project_name:
            command += f" --project {vercel_project_name}"
        
        return self._run_command(command, cwd=project_path)
    
    def add_custom_domain(
        self,
        project_name: str,
        domain: str
    ) -> Dict[str, Any]:
        """Add custom domain to Vercel project."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        command = f"vercel domains add {domain}"
        return self._run_command(command, cwd=project_path)
    
    def get_deployment_url(self, project_name: str) -> Dict[str, Any]:
        """Get the current deployment URL."""
        project_path = self.workspace_root / project_name
        
        if not project_path.exists():
            return {"success": False, "error": f"Project {project_name} not found"}
        
        result = self._run_command("vercel ls --json", cwd=project_path)
        
        if result["success"]:
            try:
                deployments = json.loads(result["stdout"])
                if deployments:
                    result["url"] = deployments[0].get("url")
            except:
                pass
        
        return result
    
    def setup_analytics(
        self,
        project_name: str,
        analytics_id: str,
        provider: str = "google"
    ) -> Dict[str, Any]:
        """Add analytics tracking to the project."""
        
        if provider == "google":
            # Add Google Analytics script to layout
            script = f'''
import Script from 'next/script'

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en">
      <head>
        <Script
          src="https://www.googletagmanager.com/gtag/js?id={analytics_id}"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {{`
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{analytics_id}');
          `}}
        </Script>
      </head>
      <body>{{children}}</body>
    </html>
  )
}}
'''
            return self.write_page_component(project_name, "layout", script)
        
        return {"success": False, "error": f"Provider {provider} not supported"}
    
    def full_launch_workflow(
        self,
        project_name: str,
        copy: Dict[str, Any],
        brand: Dict[str, Any],
        domain: Optional[str] = None,
        analytics_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Complete workflow: create, generate, build, and deploy."""
        
        results = {}
        
        # 1. Create project
        results["create"] = self.create_nextjs_project(project_name)
        if not results["create"]["success"]:
            return {"success": False, "error": "Failed to create project", "results": results}
        
        # 2. Generate landing page
        results["generate"] = self.generate_landing_page(project_name, copy, brand)
        if not results["generate"]["success"]:
            return {"success": False, "error": "Failed to generate page", "results": results}
        
        # 3. Add analytics if provided
        if analytics_id:
            results["analytics"] = self.setup_analytics(project_name, analytics_id)
        
        # 4. Install dependencies
        results["install"] = self.install_dependencies(project_name)
        if not results["install"]["success"]:
            return {"success": False, "error": "Failed to install dependencies", "results": results}
        
        # 5. Build
        results["build"] = self.build_project(project_name)
        if not results["build"]["success"]:
            return {"success": False, "error": "Failed to build project", "results": results}
        
        # 6. Deploy to Vercel
        results["deploy"] = self.deploy_to_vercel(project_name, production=True)
        if not results["deploy"]["success"]:
            return {"success": False, "error": "Failed to deploy", "results": results}
        
        # 7. Add custom domain if provided
        if domain:
            results["domain"] = self.add_custom_domain(project_name, domain)
        
        return {
            "success": True,
            "url": results["deploy"].get("url"),
            "results": results
        }
