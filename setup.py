from distutils.core import setup

setup(
    name='MontyBot',
    version='0.9.0',
    author='E N',
    author_email='esther.nam@gmail.com',
    packages=['montybot', 'montybot.plugins'],
    scripts=[],
    url='http://github.com/estherbester/montybot',
    license='LICENSE.txt',
    description='Twisted-based IRC Bot .',
    long_description=open('README').read(),
    install_requires=[
        "Twisted == 13.1.0",
        "BeautifulSoup == 3.2.1",
        "mock >= 1.0.1",
        "requests >= 0.12.0",
    ],
)
