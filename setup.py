import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_toolkit",
    version="0.0.18",
    author="Aurelio Saraiva",
    author_email="aurelio.saraiva@creditas.com.br",
    description="Flask toolkit for Domain Driven Design (DDD)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/creditas/flask-toolkit",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'marshmallow==2.15.0',
        'Flask-Log-Request-ID==0.10.0',
        'Logentries==0.17',
        'Flask-Migrate==2.1.1',
        'Flask-Cors==3.0.3',
        'Flask==1.0.2',
        'blinker==1.4',
        'event-bus==1.0.2',
        'aead==0.2',
        'flask_classful==0.14.1',
    ],
    extras_require={
        'dev':  [
            'ipdb',
            'flask-shell-ipython',
            'Flask-Script',
            'urllib3==1.22'
        ],
    }
)
