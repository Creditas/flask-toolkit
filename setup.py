import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_toolkit",
    version="0.0.4",
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
    ],
)
