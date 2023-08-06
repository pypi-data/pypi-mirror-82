from setuptools import setup

import ksoftapi


def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements


version = ksoftapi.__version__

if not version:
    raise RuntimeError('Version is not set')

with open('README.md') as f:
    readme = f.read()

setup(
    name='ksoftapi',
    packages=['ksoftapi', 'ksoftapi.apis'],
    version=version,
    description='The official KSoft.SI API Wrapper.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='AndyTempel',
    author_email='support@ksoft.si',
    url='https://github.com/KSoft-Si/ksoftapi.py',
    download_url=f'https://github.com/KSoft-Si/ksoftapi.py/archive/{version}.tar.gz',
    keywords=['ksoftapi'],
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
