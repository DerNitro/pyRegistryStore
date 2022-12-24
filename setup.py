from setuptools import setup, find_packages

setup(
    name='pyRegistryStore',
    version='0.0.9',
    url='https://github.com/DerNitro/pyRegistryStore',
    author='Sergey Utkin',
    author_email='utkins01@gmail.com',
    description='Script to view and work with the registry of objects.',
    packages=find_packages(),
    scripts=['pyRegistryStore.py'],
    install_requires=['mdutils', 'pyyaml'],
)
