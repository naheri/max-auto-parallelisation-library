from setuptools import setup, find_packages

setup(
    name="max_auto_parallelisation",
    version="0.1.0",
    author="AHAMADA Naheri",
    author_email="naheriahamada@gmail.com",
    description="Une librairie Python pour pour automatiser la parallélisation maximale de systèmes de tâches.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/votre_utilisateur/ma_librairie",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
