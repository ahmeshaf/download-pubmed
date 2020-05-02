from distutils.core import setup
setup(name='download_pubmed',
      version='1.0',
      install_requires=[
          'biopython',
            'bs4',
            'pandas'
      ],
      py_modules=['download_pubmed'],
      )
