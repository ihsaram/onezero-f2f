from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()



setup(name='FlaskApp',
      version='1.0',
      description='A basic Flask app with static files',
      author='Ryan Jarvinen',
      author_email='ryanj@redhat.com',
      url='http://www.python.org/sigs/distutils-sig/',
     install_requires=required,
     )
