# author: Drew Botwinick, Botwinick Innovations
# license: 3-clause BSD

import setuptools

with open("README.md", 'r') as f:
    readme_txt = f.read()

setuptools.setup(
    name="botwinick_sci",
    version="0.0.1",
    author="Drew Botwinick",
    author_email="foss@drewbotwinick.com",
    description="Utility functions for scientific/chemical/safety applications",
    long_description=readme_txt,
    long_description_content_type="text/markdown",
    url="https://github.com/dbotwinick/python-botwinick-sci",
    packages=setuptools.find_packages(),
    install_requires=['vpd', 'numpy', 'scipy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, >=3.6',
)
