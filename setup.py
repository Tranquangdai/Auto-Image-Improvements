import subprocess

from setuptools import setup, setuptools
from setuptools.command.install import install

__author__ = 'dai.tran'


def readme():
    with open('README.md') as f:
        return f.read()


class Command(install):

    def run(self):
        print('********************************')
        subprocess.run('pip install -r requirements.txt', shell=True)
        print('********************************')
        install.run(self)

setup(name='logohunter',
      version='0.1',
      description='Automatic Image Enhancement',
      long_description=readme(),
      long_description_content_type='text/markdown',
      author='dai tran',
      author_email='tranquangdai5@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(exclude=["tests.*", "tests", "_data"]),
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      test_suite='tests',
      tests_require=['pytest'],
      include_package_data=True,
      zip_safe=False,
      cmdclass={'install': Command, })
