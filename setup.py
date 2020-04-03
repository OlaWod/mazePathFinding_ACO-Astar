import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mazePathFinding_ACO-Astar", # Replace with your own username
    version="0.0.1",
    author="OlaWod",
    author_email="756825440@qq.com",
    description="Use A* algorithm and ant colony optimization to solve maze path finding problem.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OlaWod/mazePathFinding_ACO-Astar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
