from distutils.core import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='odinsupport',         # How you named your package folder (MyLib)
    packages=['odinsupport'],   # Chose the same as "name"
    version='0.4',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Odin support',
    long_description=readme(),
    author='eris mabu',                   # Type in your name
    author_email='phucpv89@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/phucpv89',
    # I explain this later on
    # download_url='https://github.com/phucpv89/zalopay-svn-upload/archive/v_01.tar.gz',
    # Keywords that define your package best
    keywords=['Odin'],
    install_requires=['subprocess'],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
)
