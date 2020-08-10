
# Use this command for deploy.
#   python3 setup.py sdist bdist_wheel && python3 -m twine upload --skip-existing dist/*

import io
from setuptools import find_packages, setup

setup(name='easy_glue',
      version='0.0.1',
      description='',
      long_description="Please refer to the https://github.com/da-huin/easy_glue",
      long_description_content_type="text/markdown",
      url='https://github.com/da-huin/easy_glue',
      download_url= 'https://github.com/da-huin/easy_glue/archive/master.zip',
      author='JunYeong Park',
      author_email='dahuin000@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=["boto3"],
      classifiers=[
          'Programming Language :: Python :: 3',
    ]
)


