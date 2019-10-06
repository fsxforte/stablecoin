from setuptools import setup, find_packages


setup(
    name="apollo",
    packages=find_packages(exclude=("tests",)),
    scripts=["./bin/apollo"],
    install_requires=[
        "python-binance",
        "pandas",
        "matplotlib",
        "seaborn",
        "python-dotenv",
        "tqdm",
    ],
    extras_require={
        "dev": [
            "nose",
            "pylint",
            "ipython",
        ],
    },
)