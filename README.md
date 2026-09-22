# Taejoon Park · Rekorn

Personal portfolio: https://rekorn.com/ · English: https://rekorn.com/en/

- `_data/profile.json`: public facts and source links.
- `tools/build_portfolio.py`: generates both homepages and sitemap with Python 3.
- `assets/portfolio`: styles and the owner-provided, unaltered profile photo.
- `/legacy/`: archived DJ / music site and guides. Old `/works/`, `/blog/` and
  `/neodymium-pudding/` entry URLs redirect to the archive.

GitHub Pages builds the `master` branch using the existing Jekyll archive pipeline.
The new homepages are static HTML and CSS, with no runtime JavaScript dependency.

```sh
python tools/build_portfolio.py
python -m http.server 8766 --bind 127.0.0.1
```

The local Python server previews the new homepages. Archive Liquid/Markdown requires
Jekyll; verify its rendered routes on GitHub Pages after deployment.

Original site checkpoint: `archive/dj-before-portfolio-20260923`, commit `77e6678`.
To roll back a deployment, revert the portfolio change commit; do not force-push.

Book cover and game capsules link to their official YES24/Steam sources. Their
copyright remains with the respective rights holders. The portrait is supplied by
Taejoon Park for his public professional profiles. The record graphic is CSS artwork,
not a reproduction of an album sleeve.

## Credits
### Original README from HTML5 UP
```
Massively by HTML5 UP
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)


This is Massively, a text-heavy, article-oriented design built around a huge background
image (with a new parallax implementation I'm testing) and scroll effects (powered by
Scrollex). A *slight* departure from all the one-pagers I've been doing lately, but one
that fulfills a few user requests and makes use of some new techniques I've been wanting
to try out. Enjoy it :)

Demo images* courtesy of Unsplash, a radtastic collection of CC0 (public domain) images
you can use for pretty much whatever.

(* = not included)

AJ
aj@lkn.io | @ajlkn


Credits:

	Demo Images:
		Unsplash (unsplash.com)

	Icons:
		Font Awesome (fortawesome.github.com/Font-Awesome)

	Other:
		jQuery (jquery.com)
		Misc. Sass functions (@HugoGiraudel)
		Skel (skel.io)
		Scrollex (github.com/ajlkn/jquery.scrollex)
```
