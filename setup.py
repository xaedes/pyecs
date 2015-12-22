from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="pyecs",
    version="0.0.9",
    description="Python Entity Component System Framework inspired from Unity",
    long_description=readme(),
    url="http://github.com/xaedes/pyecs",
    author="xaedes",
    author_email="xaedes@gmail.com",
    license="MIT",
    packages=["pyecs","pyecs.components"],
    dependency_links=["https://github.com/xaedes/testing/tarball/master"],
    tests_require=["pytest","pytest-mock","testing"],
    install_requires=[
        "funcy","pytest-runner"
    ],
    include_package_data=True,
    zip_safe=False
    )
