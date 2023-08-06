from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='pymatriz',
    version='0.1.3',
    packages=['pymatriz'],
    url='https://github.com/ggallohernandez/pymatriz',
    license='MIT License',
    author='Guillermo Gallo',
    author_email='ggallohernandez@gmail.com',
    description='Python connector for Primary DMA (Matriz) Rest and Websocket APIs.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
        'requests>=2.20.0',
        'simplejson>=3.10.0',
        'enum34>=1.1.6',
        'websocket-client>=0.54.0',
        'pandas~=1.1.3',
        'lxml~=4.5.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development"
    ],
)
