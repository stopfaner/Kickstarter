from setuptools import setup, find_packages

setup(
    name='kickstarter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'sanic==0.8.3',
        'Sanic-Cors==0.9.5',
        'sanic_compress==0.1.1',
        'aiohttp==3.3.2',
        'aioredis==1.1.0',
        'marshmallow==3.0.0b16',
        'gunicorn==19.8.1',
        'sqlalchemy==1.3.0b1',
        "aiopg==0.15.0",
    ],
    extras_require={
        "test": [
            'coverage==4.5.1',
        ]
    },
)
