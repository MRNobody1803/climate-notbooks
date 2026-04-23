from setuptools import setup, find_packages

setup(
    name='c3s-atlas',
    version='0.1',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "c3s-mask-africa=scripts.mask_africa:main",
        ]
    },
)
