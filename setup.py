from setuptools import setup, find_packages

setup(
    name='python_os',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'pylint',
        'black',
        'pyperclip',
    ],
)
