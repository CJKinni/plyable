from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'An llm wrapper'
LONG_DESCRIPTION = 'A package that makes it easy to build tools around the openapi llm'

setup(
    name="plyable",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Christine Kinniburgh",
    author_email="plyable@cjkinni.com",
    license='AGPLv3',
    packages=find_packages(),
    package_data={'plyable': ['plyable/*']},
    py_modules=['plyable', 'plyable.plyable', 'plyable.helpers'],
    install_requires=['openai>=0.10.0'],
    keywords='llm openai chatgpt gpt3 gpt4 gpt-3 gpt-4',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 3",
    ]
)