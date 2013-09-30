from distutils.core import setup
setup(
    name = 'AssetPackager',
    packages = ['AssetPackager'], # this must be the same as the name above
    version = '0.1.1',
    description = 'Utility for determining and making CSS/JS packages from list of paths',
    author = 'Jason Bonta',
    author_email = 'jbonta@gmail.com',
    url = 'https://github.com/jbonta/AssetPackager',   # use the URL to the github repo
    download_url = 'https://github.com/jbonta/AssetPackager/tarball/0.3', # I'll explain this in a second
    keywords = ['CSS', 'JS', 'static', 'analysis', 'dependency', 'resources'], # arbitrary keywords
    classifiers = [],
    install_requires=[
      'yuicompressor >= 2.4.7',
    ],
)
