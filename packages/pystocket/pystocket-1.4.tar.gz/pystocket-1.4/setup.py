from distutils.core import setup
setup(
  name = 'pystocket',         # How you named your package folder (MyLib)
  packages = ['pystocket'],   # Chose the same as "name"
  version = '1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Stocket API Connection Package',   # Give a short description about your library
  author = 'EvilTeliportist',                   # Type in your name
  author_email = 'stocketapi@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/EvilTeliportist/pystocket/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/EvilTeliportist/pystocket/archive/1.4.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=['requests', 'pandas', 'numpy', 'yahoo_fin', 'matplotlib'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
