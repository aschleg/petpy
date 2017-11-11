
from setuptools import find_packages, setup


setup(
    name='petpy',
    version='0.1.7',
    author='Aaron Schlegel',
    author_email='aaron@aaronschlegel.com',
    url='https://github.com/aschleg/petpy',
    description='Wrapper for the Petfinder API',
    license='MIT',
    packages=find_packages(exclude=['build', 'docs', 'tests*']),
    long_description=open('README.md').read(),
    install_requires=['requests>=2.18.4'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)