import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="magik_prompt_sdk",
    version="0.0.1",
    author="Magik Labs App Team",
    author_email="hello@magiklabs.app",
    description="SDK to interact with LLM model APIs along with prompt management and versioning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)