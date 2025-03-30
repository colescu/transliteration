from setuptools import setup

setup(
    name="transliterator",
    version="0.1",
    py_modules=["cli"],
    install_requires=[],
    entry_points={
        "console_scripts": ["tl=cli:main"],
    },
)
