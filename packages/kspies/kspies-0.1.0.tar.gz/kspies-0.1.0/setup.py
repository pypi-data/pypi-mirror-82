import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kspies", # Replace with your own username
    version="0.1.0",
    author="Seungsoo Nam,  Ryan J. McCarty, Hansol Park, Eunji Sim",
    author_email="skaclitz@yonsei.ac.kr",
    description="This is a python based Kohn-Sham Inversion Evaluation Software package for use with pySCF.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssnam92.github.io/KSPies/",
    packages=['kspies'],
    package_dir={'kspies':'kspies'},
    package_data={'kspies':['kspies_fort.f90', 'compile.sh', 'kspies_fort.cpython-37m-x86_64-linux-gnu.so']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
