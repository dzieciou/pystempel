import os

from setuptools import find_packages, setup

REQUIRED_PYTHON = [3, 5]
version = '1.1.0'


def read(fname):
    fpath = os.path.join(os.path.dirname(__file__), fname)
    with open(fpath, encoding='utf-8') as f:
        return f.read()

print(read('README.rst'))

setup(
    name='pystempel',
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    url='https://github.com/dzieciou/pystempel',
    author='Maciej Gawinecki',
    author_email='mgawinecki@gmail.com',
    description='Polish stemmer.',
    long_description=read('README.rst'),
    keywords=[
        'NLP',
        'natural language processing',
        'computational linguistics',
        'stemming',
        'linguistics',
        'language',
        'natural language',
        'text analytics',
    ],
    license='See documentation',
    packages=find_packages(exclude=['tests']),
    package_data={'': ['data/original/*.tbl.gz', 'data/polimorf/*.tbl.gz']},
    exclude_package_data={'': ['data/original/*.tbl', 'data/polimorf/*.tbl']},
    install_requires=['sortedcontainers', 'tqdm'],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
    ],
    project_urls={
        'Source': 'https://github.com/dzieciou/pystempel',
    },
)

