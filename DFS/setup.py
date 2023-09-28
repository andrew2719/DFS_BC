from setuptools import setup, find_packages

setup(
    name='DFS',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here
        # For example: 'aiofiles', 'asyncio', etc.
        'aiofiles',
        'asyncio',
        'pathlib',
    ],
)
