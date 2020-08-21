from setuptools import setup, find_packages

setup(
    name='tetracamthon',
    description="Re-engineering Tetra Pak A3 Flex filling machine's driving " +
                "cam profile with Python",
    version='v1.0',
    author='John Qu',
    author_email="johnqu1982@gmail.com",
    url="https://github.com/John-Qu/tetracamthon",
    package=find_packages(where='src'),
    package_dir={'': 'src'},
)
