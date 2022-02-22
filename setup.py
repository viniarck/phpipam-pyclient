from setuptools import setup
from phpipam_pyclient.version import __version__
desc = 'REST-client and CLI tool to interface with phpipam REST API'

setup(
    name='phipam-pyclient',
    version=__version__,
    description=desc,
    author='Vinicius Arcanjo',
    author_email='viniarck@gmail.com',
    keywords='phpipam client rest-client',
    url='http://github.com/viniarck/phpipam-pyclient',
    packages=['phpipam_pyclient'],
    license='Apache',
    install_requires=['requests>=2.19.1', 'fire>=0.1.3'],
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    entry_points='''
        [console_scripts]
        phpipam-pyclient=phpipam_pyclient.phpipam_pyclient:main
    ''',
    zip_safe=False,
)
