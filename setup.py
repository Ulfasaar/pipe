from setuptools import setup, find_packages
 
setup(name='compute_pipe',
      version='0.1',
      url='https://github.com/Ulfasaar/pipe',
      license='MIT',
      author='Ryan Weyers',
      author_email='weyers.ryan@gmail.com',
      description='A beautiful, simple, fast framework for creating computation pipelines.',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=True)