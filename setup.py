from setuptools import setup

setup(
    name="pynodelauncher",
    version="0.2.0",
    py_modules=["pynodelauncher"],
    install_requires=["mpi4py"],
    entry_points="""
        [console_scripts]
        pynodelauncher=pynodelauncher:main
    """,
)
