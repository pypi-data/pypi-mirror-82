import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riichiroyale",
    version="0.1.0",
    author="Christopher Miller",
    author_email="cmiller548@gmail.com",
    description="Singleplayer Riichi Mahjong Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HartleyAHartley/RiichiRoyale",
    packages=['libmahjong', 'riichiroyale'],
    package_dir={'libmahjong': '.'},
    package_data={'libmahjong': ['libmahjong.pyd'], 'riichiroyale': ['riichiroyale/resources/theme.json', 'riichiroyale/*', 'riichiroyale/**/*', 'riichiroyale/**/**/*', 'riichiroyale/resources/**/**/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
    entry_points={
        'console_scripts':['riichiroyale=riichiroyale.__main__:main']
    },
    include_package_data=True,
    python_requires='>=3.6',
)
