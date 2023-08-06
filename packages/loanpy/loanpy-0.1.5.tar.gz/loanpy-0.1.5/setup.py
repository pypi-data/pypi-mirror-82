import setuptools

def readme():
	with open("README.rst") as f:
		README = f.read()
	return README

setuptools.setup(
    name="loanpy",
    version="0.1.5",
    author="Viktor Martinović",
    author_email="viktor.martinovic@hotmail.com",
    description="framework for detecting old loanwords",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    url="https://github.com/martino-vic/Framework-for-computer-aided-borrowing-detection",
    license="Creative Commons Attribution 4.0 International",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    keywords="historical linguistics, computational linguistics, lexicology, evolution, Uralistics, borrowing detection",
    project_urls={
        "Source": "https://github.com/martino-vic/Framework-for-computer-aided-borrowing-detection",
        "Citation": "http://doi.org/10.5281/zenodo.4009627",
    },
    packages=["loanpy"],
    package_dir={"loanpy": "loanpy"},
    package_data={"loanpy": ["loanpy/data/*.csv"]},
    include_package_data=True,
    install_requires=["pandas","lingpy","nltk","epitran","gensim","bs4","pdfminer"],
    python_requires='>=3.6',
)