from setuptools import setup

# Impostazioni per permettere alla libreria Click di riconoscere i comandi

setup(
    name='Articlee-CLI',
    version='1.0',
    packages=['cli', 'cli.commands'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points="""
        [console_scripts]
        articlee=cli.cli:cli
    """,
)