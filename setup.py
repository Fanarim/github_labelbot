#!/usr/bin/env python3.5

from setuptools import setup, find_packages

with open('README.rst') as readme:
    long_description = ''.join(readme.readlines())

setup(
    name='github-labelbot',
    version='0.3.0',
    description='Simple bot labeling GitHub issues based on it\'s configuration. ',
    long_description=long_description,
    author='David Viktora',
    author_email='viktoda2@fit.cvut.cz',
    keywords='github, bot, issues',
    license='MIT License',
    url='https://github.com/fanarim/github_labelbot',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=['click==6.6',
                      'decorator==4.0.10',
                      'Flask==0.11.1',
                      'itsdangerous==0.24',
                      'Jinja2==2.8',
                      'MarkupSafe==0.23',
                      'requests==2.11.1',
                      'six==1.10.0',
                      'validators==0.11.0',
                      'Werkzeug==0.11.11'],
    entry_points={
        'console_scripts': [
            'labelbot = labelbot.run:main',
        ],
    },
    package_data={
        'labelbot': [
            'static/custom.css',
            'templates/index.html'
        ]
    },
)
