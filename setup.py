from setuptools import setup, find_packages


long_description = 'SSHSelect - hosts manager for shell. Simple hosts picker for ssh, more ine README file'


setup(
    name='sshs',  # name your package
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        "console_scripts": [
            "sshs=sshs:cli"
        ]
    },
    version='1.0.0',
    description='SSHSelect - hosts manager for shell',
    long_description=long_description,
    author='tssan',
    author_email='piotr.karasinski@gmail.com',
    license='Apache License 2.0',  # choose the appropriate license
    install_requires=[
        'Click==7.0'
    ],
    python_requires='>=3.5'
)
