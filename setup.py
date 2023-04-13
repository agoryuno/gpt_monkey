from setuptools import setup, find_packages

setup(
    name="gpt_monkey",
    version="0.1.0",
    author="Alex Goryunov",
    author_email="alex.goryunov@gmail.com",
    description="A package for interacting with GPT-Monkey",
    url="https://github.com/agoryuno/gpt_monkey",
    packages=find_packages("src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests",
    ],
)
