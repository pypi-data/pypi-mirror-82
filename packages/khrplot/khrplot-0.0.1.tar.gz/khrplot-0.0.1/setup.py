from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='khrplot',
  version='0.0.1',
  description='import google sheets and plot any columns you choose',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Hemanth Reddy',
  author_email='hemanthreddy.kolli@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='plots', 
  packages=find_packages(),
  install_requires=['pandas','gspread','matplotlib','oauth2client.service_account'] 
)