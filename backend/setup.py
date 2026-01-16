from setuptools import setup, find_packages

setup(
    name="founder-autopilot",
    version="0.1.0",
    packages=find_packages(include=["app", "app.*"]),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "openai>=1.10.0",
        "stripe>=7.0.0",
        "playwright>=1.40.0",
        "python-multipart>=0.0.6",
        "aiofiles>=23.2.1",
        "httpx>=0.26.0",
        "python-dotenv>=1.0.0",
        "sqlalchemy>=2.0.25",
        "alembic>=1.13.1",
        "cryptography>=41.0.7",
        "google-cloud-compute>=1.15.0",
        "google-cloud-run>=0.10.0",
        "google-cloud-secret-manager>=2.16.0",
        "google-api-python-client>=2.100.0",
        "requests>=2.31.0",
    ],
)
