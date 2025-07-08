from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name='file_converter',
    version='1.0.0',
    author='File Converter Team',
    author_email='contact@example.com',
    description='A versatile, extensible file converter supporting multiple formats',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/santilanzb/File_converter',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'fconv=main:main',
        ],
    },
    keywords='file converter, format conversion, csv, json, pdf, docx, pptx',
    zip_safe=False,
)
