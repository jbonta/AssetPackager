from distutils.core import setup
setup(
    name = 'AssetPackager',
    packages = ['AssetPackager'],
    version = '0.2.1',
    description = 'Utility for determining and making CSS/JS packages from list of paths',
    author = 'Jason Bonta',
    author_email = 'jbonta@gmail.com',
    url = 'https://github.com/jbonta/AssetPackager',
    download_url = 'https://github.com/jbonta/AssetPackager/tarball/0.2.1',
    keywords = ['CSS', 'JS', 'static', 'analysis', 'dependency', 'resources'],
    classifiers = [],
    install_requires=[
      'yuicompressor >= 2.4.7',
    ],
)
