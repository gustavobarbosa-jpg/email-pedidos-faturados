"""
Setup do Pipeline de Relatórios por Email
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="email-pedidos-faturados",
    version="1.0.0",
    author="Gustavo Barbosa",
    author_email="gustavo.barbosa@vilanova.com.br",
    description="Pipeline de relatórios de pedidos faturados com integração Power BI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavobarbosa/email-pedidos-faturados",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-pipeline=main:main",
            "email-scheduler=schedule_pipeline:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.bat", "*.md", "*.txt"],
    },
)
