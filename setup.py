from setuptools import setup, find_packages

setup(
    name='tetracamthon',
    description="Re-engineering Tetra Pak A3 Flex filling machine's driving " +
                "cam profile with Python",
    version='v1.1',
    author='John Qu',
    author_email="johnqu1982@gmail.com",
    url="https://github.com/John-Qu/tetracamthon",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)

setup(
    name='a3flex',
    description="Regenerate the pvaj plot from the graph of Tetra Pak A3 Flex "
                "filling machine's driving cam's acceleration",
    version='v1.1',
    author='John Qu',
    author_email="johnqu1982@gmail.com",
    url="https://github.com/John-Qu/tetracamthon",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
