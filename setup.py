from setuptools import setup, find_packages

setup(
    name='gpx2maps',
    version='0.1.0',
    description='CLI tool to scrape GPX routes and convert them to Google Maps',
    author='Pieter Kuppens',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0,<3.0.0',
        'beautifulsoup4>=4.12.0,<5.0.0',
        'gpxpy>=1.6.0,<2.0.0',
        'googlemaps>=4.10.0,<5.0.0',
        'lxml>=4.9.0,<6.0.0',
    ],
    entry_points={
        'console_scripts': [
            'gpx2maps=gpx2maps.cli:main',
        ],
    },
    python_requires='>=3.7',
)
