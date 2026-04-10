from setuptools import setup, find_packages

setup(
    name="clinical-validators",
    version="0.1.0",
    description="Clinical calculation validators - verified reference implementations",
    author="Timothy Hartzog, MD",
    author_email="timothy@hartzog.me",
    url="https://github.com/timothyhartzog/clinical-calc-validators",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.22.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ]
    },
)
