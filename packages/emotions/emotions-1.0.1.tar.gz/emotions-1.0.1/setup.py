# -*- coding: utf-8 -*-
"""setup.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V8VTJdp-oylfcE4_vL_LDoYNsTvgnwfG
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="emotions",
 
    #version of the module
    version="1.0.1",
 
    #Name of Author
    author="Anurag Dutta",
 
    #your Email address
    author_email="mlmajumder4@gmail.com",
 
    #Small Description about module
    description="This is a Program which can simulate EMOTIONS and MOOD.",
 
    long_description=long_description,
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    #url="https://twitter.com/AnuragDutta_",
    packages=setuptools.find_packages(),
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)