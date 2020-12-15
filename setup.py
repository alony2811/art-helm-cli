from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='helmcli',
    version='0.1.0',
    description='CLI deploying artifactory latest chart with override params',
    log_description=readme,
    author='AlonYaron',
    author_email='alony@jfrog.com',
    install_requires=[],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'helmcli='
            'helmcli=helmcli:main',
        ],
    },
)