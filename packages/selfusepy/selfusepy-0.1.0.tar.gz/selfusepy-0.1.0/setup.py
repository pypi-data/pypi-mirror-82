from setuptools import setup, find_packages

version = '0.1.0'

# set README as long description
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'selfusepy',
    version = version,
    license = 'Apache-2.0',
    author = 'Luoming Xu',
    author_email = 'xjy46566696@gmail.com',
    description = 'Self-Use Python lib',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/LuomingXu/selfusepy',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Customer Service',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Typing :: Typed'
    ],
    python_requires = '>=3.7',
)
