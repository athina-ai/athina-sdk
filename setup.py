import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="magik",
    version="0.2.7",
    author="Magik Labs Team",
    author_email="hello@magiklabs.app",
    description="SDK to write and run tests for your LLM app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "magik=magik.cli:main",
        ],
    },
    python_requires=">=3.6",
)
