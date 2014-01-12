from setuptools import setup

setup(
    name = "greek-accentuation",
    version = "0.3",
    description = "Python 3 library for accenting (and analyzing the accentuation of) Ancient Greek words",
    license = "MIT",
    url = "http://github.com/jtauber/greek-accentuation",
    author = "James Tauber",
    author_email = "jtauber@jtauber.com",
    py_modules = ["characters", "syllabify", "accentuation"],
)
