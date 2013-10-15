from distutils.core import setup

setup(
    name='GSMT',
    version='1.3.2',
    author='Filip Dobrovolny',
    author_email='brnopcman@gmail.com',
    packages=['GSMT'],
    scripts=['bin/gsmt-configure', 'bin/gsmt'],
    url='www.google.com',
    license='LICENSE.txt',
    description='GSMT - Game Server Managment Tool \n Useful tool for server managment.',
    long_description='GSMT - Game Server Managment Tool \n Useful tool for server managment.',#open('README.txt').read(),
    install_requires=[
        "sqlite3",
    ],
)