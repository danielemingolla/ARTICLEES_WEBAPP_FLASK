from setuptools import setup
'''
 Per far riconoscere il comando 'articlee' è necessario
 eseguire prima il comando 'python -m pip install -e .'
 e
'''
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
