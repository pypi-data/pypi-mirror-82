from distutils .core import setup

setup(
  name = "snakebooru",         # How you named your package folder (MyLib)
  packages = ["snakebooru"],   # Chose the same as "name"
  version = "0.3.4",      # Start with a small number and increase it with every change you make
  license="gpl-3.0",        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Module to access various booru sites APIs.",   # Give a short description about your library
  author = "berryytf",                   # Type in your name
  author_email = "gabe@kjsl.org",      # Type in your E-Mail
  url = "https://github.com/berryytf/snakebooru",   # Provide either the link to your github or to your website
  download_url = "https://github.com/berryytf/snakebooru/archive/v0.3.3-alpha.tar.gz",    # I explain this later on
  keywords = ["Booru", "Anime", "Imageboard", "NSFW"],   # Keywords that define your package best
  install_requires=[
    "furl",
    "aiohttp"
  ],
  classifiers=[
    "Development Status :: 3 - Alpha",      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    "Intended Audience :: Developers",      # Define that your audience are developers
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",   # Again, pick a license
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8"
  ],
)