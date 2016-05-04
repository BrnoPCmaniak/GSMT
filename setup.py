from distutils.core import setup

setup(
    name='GSMT',
    version='2.0.0',
    author='Filip Dobrovolny',
    author_email='brnopcman@gmail.com',
    packages=['GSMT'],
    scripts=['bin/gsmt-daemon', 'bin/gsmt'],
    url='https://github.com/BrnoPCmaniak/GSMT',
    license='docs/LICENSE.txt',
    description='GSMT - Game Server Managment Tool \n Useful tool for server managment.',
    long_description=open('README.md').read(),
    install_requires=[
        "daemonize",
        "configargparse",
        "configparser",
        "future",
    ],
)
