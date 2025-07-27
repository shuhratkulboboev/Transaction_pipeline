from setuptools import setup, find_packages

setup(
    name="transaction_pipeline",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'python-dateutil>=2.8.2',
    ],
    entry_points={
        'console_scripts': [
            'transaction-pipeline=src.cli:main',
        ],
    },
)