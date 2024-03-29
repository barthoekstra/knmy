from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.5.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='knmy',
    version=__version__,
    description='Python package for downloading and processing weather data from the automated weather stations of the Dutch Meteorological Institute (KNMI).',
    long_description=long_description,
    url='https://github.com/barthoekstra/knmy',
    download_url='https://github.com/barthoekstra/knmy/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['mock', 'pytest', 'sh>=1.08'],
    author='Bart Hoekstra',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='barthoekstra@gmail.com',
    python_requires='>=3.4',
)
