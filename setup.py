import setuptools

setuptools.setup(
    name="efictopub",
    packages=setuptools.find_packages(),
    install_requires=[
        "praw",
        "mkepub",
        "bs4",
        "lxml",
        "requests",
        "dulwich",
        "jsonpickle",
        "svgwrite",
        "confuse",
    ],
    entry_points={"console_scripts": ["efictopub = efictopub.__main__:main"]},
)
