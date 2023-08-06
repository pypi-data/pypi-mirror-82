from distutils.core import setup
setup(
  name = 'higradpy',         # How you named your package folder (MyLib)
  packages = ['higradpy'],   # Chose the same as "name"
  version = '0.11',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python Implementation of Hierarchical Incremental Gradient Descent',   # Give a short description about your library
  long_description="gaand me danda de...",
  long_description_content_type="text/markdown",
  author = 'Vihan Singh',                   # Type in your name
  author_email = 'vihan13singh@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/vihan13singh',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vihan13singh/higradpy/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['Statistical Inference', 'Machine Learning', 'Stochastic Gradient Descent'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'matplotlib',
          'scikit-learn',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)