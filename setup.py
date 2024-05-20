from setuptools import setup, find_packages

setup(
    name='redirect_checker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
        'urllib3',
    ],
    entry_points={
        'console_scripts': [
            'redirect_checker=redirect_checker:main',
        ],
    },
    description='A tool to check URL redirects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/redirect_checker',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
