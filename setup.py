from setuptools import setup, find_packages
 
setup(name='compute_pipe',
      version='0.1-alpha',
      url='https://github.com/Ulfasaar/pipe',
      license='MIT',
      author='Ryan Weyers',
      author_email='weyers.ryan@gmail.com',
      description='A beautiful, simple, fast framework for creating computation pipelines.',
      long_description=open('README.md').read(),
      packages=find_packages(include=['.'], exclude=['tests', '*test*.py', 'test.py']),
      zip_safe=True)