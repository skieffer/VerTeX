import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vertex2tex",
    version="0.3.3",
    license="MIT",
    author="Steve Kieffer",
    author_email="sk@skieffer.info",
    description="VerTeX: Verbal TeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skieffer/VerTeX",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
)

