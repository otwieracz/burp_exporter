from setuptools import setup, find_packages

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(name='burp_exporter',
      version='0.1',
      description='Simple burp (backup) prometheus metric exporter',
      author='Slawomir Gonet',
      author_email='slawek@otwiera.cz',
      url='https://github.com/otwieracz/burp_exporter',
      packages=find_packages(),
      install_requires=requirements,
      entry_points = {
          'console_scripts': ['burp_exporter=burp_exporter.exporter:start_exporter']
      },
      python_requires='>=3.6',
      )
