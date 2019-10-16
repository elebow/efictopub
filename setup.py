import setuptools

setuptools.setup(
    name="efictopub",
    packages=setuptools.find_packages(),
    install_requires=[
        "praw",
        "mkepub",
        "bs4",
        "requests",
        "dulwich",
        "jsonpickle",
        "svgwrite",
        "confuse",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "doubles",
        "factory-boy",
        "pytest-factoryboy",
    ],
    entry_points={"console_scripts": ["efictopub = efictopub.__main__:main"]},
)
