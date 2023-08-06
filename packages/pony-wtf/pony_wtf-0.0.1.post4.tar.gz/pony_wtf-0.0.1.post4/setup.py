# python setup.py sdist upload # working
from setuptools import setup, find_packages


def readme():
    with open('pony_wtf/README.rst') as f:
        return f.read()


#packages = find_packages('pony_wtf')
#print (packages)

setup(name='pony_wtf',
      version='0.0.1.post4',
      description='Create WTF-Form from your pony database entity',
      long_description=readme(),
      #long_description_content_type="text/markdown",
      classifiers=[
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.7 :: Python :: 3.8',
        #'Topic :: Text Processing :: Linguistic',
      ],
      keywords='pony ponyorm wtf wtf-form ',
      license='MIT',
      url='https://github.com/tabebqena/Pony-WTF',
      author='Ahmad Yahia',
      author_email='qenadev@gmail.com',
      package_dir={'': '.'},
      packages= [ "pony_wtf", "pony_wtf/fields"], #packages,#["pony_wtf"],
      install_requires=[
          'pony',
          'pony_wtf',
          'Flask_WTF',
          'WTForms',
      ],
      include_package_data=True,
      zip_safe=False,
      #zip_ok=False,
      )

