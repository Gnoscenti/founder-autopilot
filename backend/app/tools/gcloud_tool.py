"""Google Cloud tool - cloud infrastructure operations with CLI and API modes."""
from typing import Dict, Any, Optional, List
import subprocess
import json
from pathlib import Path


class GCloudTool:
    """Tool for Google Cloud operations supporting both CLI and API modes."""
    
    def __init__(self, mode: str = "cli", credentials_path: Optional[str] = None):
        """
        Initialize GCloud tool.
        
        Args:
            mode: "cli" for gcloud CLI or "api" for direct API calls
            credentials_path: Path to service account JSON (for API mode)
        """
        self.mode = mode
        self.credentials_path = credentials_path
        
        if mode == "api" and credentials_path:
            self._init_api_client()
    
    def _init_api_client(self):
        """Initialize Google Cloud API clients."""
        try:
            from google.oauth2 import service_account
            from googleapiclient import discovery
            
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            
            self.compute = discovery.build('compute', 'v1', credentials=credentials)
            self.run = discovery.build('run', 'v1', credentials=credentials)
            self.cloudresourcemanager = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
            self.iam = discovery.build('iam', 'v1', credentials=credentials)
            self.secretmanager = discovery.build('secretmanager', 'v1', credentials=credentials)
            
        except ImportError:
            print("Warning: google-cloud libraries not installed. Install with: pip install google-cloud-compute google-cloud-run google-cloud-secret-manager")
        except Exception as e:
            print(f"Warning: Could not initialize GCloud API client: {e}")
    
    def _run_gcloud(self, args: List[str], timeout: int = 60) -> Dict[str, Any]:
        """Run gcloud CLI command."""
        try:
            result = subprocess.run(
                ['gcloud'] + args,
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
        
        except FileNotFoundError:
            return {"success": False, "error": "gcloud CLI not found. Install from: https://cloud.google.com/sdk/docs/install"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Project Management
    
    def create_project(self, project_id: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Create a new GCP project."""
        if self.mode == "cli":
            args = ['projects', 'create', project_id]
            if project_name:
                args.extend(['--name', project_name])
            return self._run_gcloud(args)
        else:
            # API mode implementation
            return {"success": False, "error": "API mode not fully implemented"}
    
    def set_project(self, project_id: str) -> Dict[str, Any]:
        """Set active project."""
        if self.mode == "cli":
            return self._run_gcloud(['config', 'set', 'project', project_id])
        else:
            return {"success": False, "error": "API mode not applicable for this operation"}
    
    def get_project(self) -> Dict[str, Any]:
        """Get current project."""
        if self.mode == "cli":
            result = self._run_gcloud(['config', 'get-value', 'project'])
            if result["success"]:
                result["project_id"] = result["stdout"].strip()
            return result
        else:
            return {"success": False, "error": "API mode not applicable for this operation"}
    
    # API Management
    
    def enable_api(self, api_name: str, project_id: Optional[str] = None) -> Dict[str, Any]:
        """Enable a GCP API."""
        if self.mode == "cli":
            args = ['services', 'enable', api_name]
            if project_id:
                args.extend(['--project', project_id])
            return self._run_gcloud(args, timeout=120)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    def enable_common_apis(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """Enable commonly needed APIs for web apps."""
        apis = [
            'run.googleapis.com',           # Cloud Run
            'cloudbuild.googleapis.com',    # Cloud Build
            'secretmanager.googleapis.com', # Secret Manager
            'sqladmin.googleapis.com',      # Cloud SQL
            'storage-api.googleapis.com',   # Cloud Storage
            'cloudresourcemanager.googleapis.com',
        ]
        
        results = []
        for api in apis:
            result = self.enable_api(api, project_id)
            results.append({"api": api, "result": result})
        
        return {
            "success": all(r["result"]["success"] for r in results),
            "results": results
        }
    
    # Service Accounts
    
    def create_service_account(
        self,
        account_id: str,
        display_name: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a service account."""
        if self.mode == "cli":
            args = ['iam', 'service-accounts', 'create', account_id, '--display-name', display_name]
            if project_id:
                args.extend(['--project', project_id])
            return self._run_gcloud(args)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    def create_service_account_key(
        self,
        account_email: str,
        key_file: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create and download service account key."""
        if self.mode == "cli":
            args = ['iam', 'service-accounts', 'keys', 'create', key_file, '--iam-account', account_email]
            if project_id:
                args.extend(['--project', project_id])
            return self._run_gcloud(args)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    # Secret Manager
    
    def create_secret(
        self,
        secret_id: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a secret in Secret Manager."""
        if self.mode == "cli":
            args = ['secrets', 'create', secret_id, '--replication-policy', 'automatic']
            if project_id:
                args.extend(['--project', project_id])
            return self._run_gcloud(args)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    def add_secret_version(
        self,
        secret_id: str,
        data: str,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a version to a secret."""
        if self.mode == "cli":
            # Use echo to pipe data
            args = ['secrets', 'versions', 'add', secret_id, '--data-file=-']
            if project_id:
                args.extend(['--project', project_id])
            
            try:
                result = subprocess.run(
                    ['gcloud'] + args,
                    input=data,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    # Cloud Run
    
    def deploy_cloud_run(
        self,
        service_name: str,
        image: str,
        region: str = "us-central1",
        allow_unauthenticated: bool = True,
        env_vars: Optional[Dict[str, str]] = None,
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Deploy a service to Cloud Run."""
        if self.mode == "cli":
            args = [
                'run', 'deploy', service_name,
                '--image', image,
                '--region', region,
                '--platform', 'managed',
            ]
            
            if allow_unauthenticated:
                args.append('--allow-unauthenticated')
            
            if env_vars:
                env_str = ','.join([f"{k}={v}" for k, v in env_vars.items()])
                args.extend(['--set-env-vars', env_str])
            
            if project_id:
                args.extend(['--project', project_id])
            
            return self._run_gcloud(args, timeout=300)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    def get_cloud_run_url(
        self,
        service_name: str,
        region: str = "us-central1",
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the URL of a Cloud Run service."""
        if self.mode == "cli":
            args = [
                'run', 'services', 'describe', service_name,
                '--region', region,
                '--format', 'value(status.url)'
            ]
            
            if project_id:
                args.extend(['--project', project_id])
            
            result = self._run_gcloud(args)
            if result["success"]:
                result["url"] = result["stdout"].strip()
            return result
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    # Cloud Storage
    
    def create_bucket(
        self,
        bucket_name: str,
        location: str = "us-central1",
        project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a Cloud Storage bucket."""
        if self.mode == "cli":
            args = ['storage', 'buckets', 'create', f"gs://{bucket_name}", '--location', location]
            if project_id:
                args.extend(['--project', project_id])
            return self._run_gcloud(args)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    def upload_to_bucket(
        self,
        local_path: str,
        bucket_name: str,
        destination_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload file to Cloud Storage bucket."""
        if self.mode == "cli":
            dest = f"gs://{bucket_name}/{destination_path or Path(local_path).name}"
            args = ['storage', 'cp', local_path, dest]
            return self._run_gcloud(args)
        else:
            return {"success": False, "error": "API mode not fully implemented"}
    
    # Authentication
    
    def auth_login(self) -> Dict[str, Any]:
        """Trigger browser-based authentication (human required)."""
        if self.mode == "cli":
            return self._run_gcloud(['auth', 'login'])
        else:
            return {"success": False, "error": "API mode uses service account credentials"}
    
    def auth_application_default_login(self) -> Dict[str, Any]:
        """Set up application default credentials."""
        if self.mode == "cli":
            return self._run_gcloud(['auth', 'application-default', 'login'])
        else:
            return {"success": False, "error": "API mode uses service account credentials"}
    
    # Utility
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get current authenticated account."""
        if self.mode == "cli":
            result = self._run_gcloud(['auth', 'list', '--format', 'json'])
            if result["success"]:
                try:
                    result["accounts"] = json.loads(result["stdout"])
                except:
                    pass
            return result
        else:
            return {"success": False, "error": "API mode not applicable"}
