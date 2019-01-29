from setuptools import setup, find_packages

setup(
    name='m_covers',
    version='0.0.1',
    packages=find_packages(exclude='venv'),
    url='',
    license='MIT',
    author='kuronbo',
    author_email='kurinbo.i2o@gmail.com',
    description='book cover storage for `mymemory`',
    install_requires=['SQLAlchemy',
                      'requests'
                      ]
)
