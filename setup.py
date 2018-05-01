from setuptools import setup

setup(
    name='bestnewmusic',
    description='View editor selections from music review sites in the terminal',
    url='http://github.com/ddbourgin/bestnewmusic',
    version='0.1',
    author='David Bourgin',
    author_email='ddbourgin@gmail.com',
    license='MIT',
    packages=['bestnewmusic'],
    entry_points = {
        "console_scripts": [
            "bnm = bestnewmusic.__main__:main",
        ]
    },
    install_requires=[
        'requests',
        'termcolor',
        'beautifulsoup4',
        'html5lib',
        'selenium'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False,
    include_package_data=True,
)
