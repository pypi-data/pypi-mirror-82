import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oscli",
    version="0.0.2",
    author="Krzysztof Ś",
    author_email="papierukartka@gmail.com",
    description="OpenSubtitles CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/papierukartka/oscli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        oscli=oscli.main:cli
    ''',
    python_requires='>=3.6',
)
