from setuptools import setup, find_packages

"""
This file makes the project installable.
By installing it, Python's environment will always know where to find the
'core' and 'plugins' modules, resolving import errors permanently.
"""

setup(
    # The name of your package
    name='file_converter',
    
    # The version
    version='0.1.0',
    
    # This command automatically finds all packages (directories with __init__.py)
    # We specify the 'where' argument to be the current directory.
    packages=find_packages(where='.'),
    
    # This tells setuptools that the root of the package is the current directory.
    # This is a key change to help resolve the module path.
    package_dir={'': '.'},
    
    # This is the magic part: it creates a command-line script for us.
    # We're telling it to create a command called 'fconv' that runs the
    # 'main' function inside our 'file_converter/main.py' script.
    entry_points={
        'console_scripts': [
            'fconv = file_converter.main:main',
        ],
    },

    # Setting zip_safe to False can help with compatibility in some environments.
    zip_safe=False,
)
