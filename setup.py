from setuptools import setup

setup(
    name="greek-accentuation",
    version="0.9.7",
    description="""\
Python 3 library for accenting (and analyzing the accentuation of) \
Ancient Greek words""",
    license="MIT",
    url="http://github.com/jtauber/greek-accentuation",
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    py_modules=["characters", "syllabify", "accentuation"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Text Processing :: Linguistic",
    ],
)
