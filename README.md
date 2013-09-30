AssetPackager
=============

AssetPackager is a python utility for determining and making CSS/JS packages from list of paths. It's designed to help out static website generators like [Cactus](https://github.com/koenbok/Cactus) decide how to package static resources intelligently. 

## The Goal

You want to serve your website with as few static resources as possible, because with each one comes overhead of an HTTP request. However, it's hard to generalize this and put everything in one giant package, lest you over-include data for parts of your site that you don't need.

AssetPackager takes a simple, conservative approach to finding a minimal set of packages needed to render the pages in your site without including more than you need to on any page.

## Features
- Concatenation of multiple source files into one, intelligently
- Compression of CSS and JS using [YUI Compressor](https://pypi.python.org/pypi/yuicompressor/2.4.2)
- Markers in the source to see where different parts of the concatenated files came from
- Support for remotely-hosted assets. AssetPackager downloads and outputs them into your packages
- Order preservation of assets


## Example Usage

###Analyzing assets.
- Include a list of "pages". Each "page" itself is just a list of paths pulled in on that page.
- Keep CSS and JS lists separate.

Calling:

	AssetPackager.analyze(
	  [
	    ['/static/jquery.js', '/static/sitecore.js', '/foo/stuff/lost.js'],
	    ['/static/jquery.js', '/static/sitecore.js', '/foo/stuff/found.js'],
	    ['/static/errorPage.css', '/static/404.css'],
	    ['/static/jquery.js', '/static/sitecore.js', 'http://ajax.googleapis.com/ajax/libs/webfont.js'],
	    ['/static/jquery.js', '/static/sitecore.js'],
	    ['/static/jquery.js', '/static/sitecore.js']
	  ]
	 )

...results in a list of "buckets" that can be safely packaged:

	[
      ['/static/jquery.js', '/static/sitecore.js'],
      ['/foo/stuff/lost.js'],                      
      ['/foo/stuff/found.js'],                     
      ['/static/errorPage.css', '/static/404.css']
	]
	
- From here, you can know, given an original asset, which bucket it should fall in.
	
###Packaging assets.
- If you know how your assets should be packaged (or if you've already used `AssetPackager.analyze`, you can do the actual packaging like this:
- `AssetPackager.package(<list_of_paths>, <output_path_filename>, compress=True, filename_markers_in_comments=True)`

Calling:

	AssetPackager.package(
      ['/static/errorPage.css', '/static/404.css'],
      '/static/errorPage_404_merged.css',
      compress=True,
      filename_markers_in_comments=True
    )

...will save the following output to `/static/errorPage_404_merged.css`:
  
    /* errorPage.css ---------------------------------------- */
      ...
  
    /* 404.css ---------------------------------------- */
      ...

## Installing
Simply install with:

    pip install AssetPackager
    
then import:

    import AssetPackager
    
That's it!
