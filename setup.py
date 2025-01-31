from setuptools import setup, find_packages

setup(
    name="stock_insight",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "akshare",
        "pandas",
        "sqlalchemy",
        "psycopg2-binary",
        "python-dotenv",
    ],
)