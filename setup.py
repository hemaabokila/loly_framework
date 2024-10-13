from setuptools import setup, find_packages

setup(
    name='loly-framework',
    version='1.0.0',
    author='Ibrahem Abo Kila',
    author_email='ibrahemabokila@gmail.com',
    description='A security framework for testing web applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hemaabokila/loly_framework',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'cmd2',
        'colorama',
        'dnspython', 
        'asyncio',
        'rich',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        '': [
            'wordlists/*.txt',
            'payloads/*.txt',
            'configs/*.txt',
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'loly=core.cli:run',
        ],
    },
)
