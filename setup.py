from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="google-api-toolkit-commons",
    version="0.2.7",
    author="Alexandre Cox",
    author_email="developpeur@phytochemia.com",
    description="Common assets for the google-api-toolkit package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    install_requires=[
        "google-api-python-client==1.7.11",
        "pydantic==1.5",
        "typing_extensions",
    ],
    packages=["google_api_toolkit.commons"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
