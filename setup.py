config = {
    "description":
    "Regetron3.0 is a simple shell for playing with regular expressions.",
    "author": "Sean Marshallsay",
    "url": "https://github.com/Sean1708/Regetron3.0.git",
    "download_url": "",
    "author_email": "srm.1708@gmail.com",
    "version": "0.0",
    "install_requires": [],
    "packages": ["regetron"],
    "name": "Regetron3.0"
}

try:
    from setuptools import setup

    config["entry_points"] = {
        "console_scripts": ["regetron = regetron.cmdline:main"],
    }

except ImportError:
    from distutils.core import setup

    config["scripts"] = ["bin/regetron", "bin/regetron.bat"]

setup(**config)
