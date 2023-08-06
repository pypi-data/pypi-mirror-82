import os
from codecs import open

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
  name = 'electricalcalc',         
  packages = ['electricalcalc'],
  version = '0.1',
  license='MIT',
  description = 'This is the package that houses various functions which can be used to calculate values for problems involving circuit design , value of the components which are needed to construct the circuit and so on',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = ['Vishal Balaji Sivaraman','Vigneshwar K R','Sanjay Rajavel'],
  author_email = 'vb.sivaraman_official@yahoo.com',
  url = 'https://github.com/The-SocialLion/electricalcalc',
  download_url = 'https://github.com/The-SocialLion/electricalcalc/archive/master.zip',
  keywords = ['ELECTRICAL', 'CALCULATOR', 'ELECTRICAL-CALCULATIONS','CIRCUIT-DESIGN','PLOT'],   
  install_requires=[           
          'numpy',
          'pandas',
          'Matplotlib',
          'SciPy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
