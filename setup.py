import setuptools

with open("README.md", "rt", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PyAutoMaker",
    version = "0.1.5",
    author = "WDW",
    author_email = "boa9448@naver.com",
    description = "자동화를 위한 패키지",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/boa9448/PyAutoMaker",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],

    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    package_data = { "PyAutoMaker" : ["dlls/*"] },
    install_requires = ["psutil", "keyboard", "mouse", "pywin32", "opencv-contrib-python==4.5.4.58", "tensorflow", "pySerial"],

    python_requires = '>=3.6',
)