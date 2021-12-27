from setuptools import setup

setup(
    name='durgod',
    version='0.1.0',
    author='Ilia Pozdnyakov',
    author_email='ilia.pozdnyakov@ya.ru',
    url='https://github.com/iliazeus/durgod',
    license='MIT',

    packages=['durgod'],
    install_requires=[
        'pyusb >= 1.0',
    ],
)
