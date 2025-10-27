from setuptools import setup, find_packages

setup(
    name="finance-copilot",
    version="0.1.0",
    description="AI-powered financial assistant for Cash App-style transaction analysis",
    author="Finance Copilot Team",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
    python_requires=">=3.8",
)
