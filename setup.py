from setuptools import setup

setup(
    name="greek-accentuation",
    version="1.1.1",
    description="""\
Python 3 library for accenting (and analyzing the accentuation of) \
Ancient Greek words""",
    license="MIT",
    url="http://github.com/jtauber/greek-accentuation",
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    packages=["greek_accentuation"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing :: Linguistic",
    ],
)
