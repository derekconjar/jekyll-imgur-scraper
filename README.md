Jekyll Imgur Scraper
====================

This is a simple Python script that scrapes all the Imgur images for a particular subreddit and creates search engine friendly Jekyll posts and thumbnails.

Technically it should work for any static site generator that supports Jekyll-style YAML frontmatter, such as Middleman. And it's easy to tweak the output so it supports other formats, like Pelican's metadata syntax.

First install the dependencies:

```
$ pip install pillow
$ pip install imgurpython
```

Next, `cd` into your Jekyll project directory and create folders to store your image downloads and thumbnails:

```
$ cd jekyll_project
$ mkdir downloads
$ mkdir thumbs
```

Add your imgur API credentials and run the script in your working directory with `python jekyll_imgur_scraper.py`.

It'll ask you what subreddit you want to scrape, and what page you want to start scraping (the latest pics on Imgur being page 0).

Answer those questions and it'll start scraping all the photos. The filenames and post slugs are based on the title of the picture. So a 600px wide image named "Cat Picture" is saved to `./downloads/cat-picture-600.jpg`, a 300x300px thumbnail is saved to `./thumbs/cat-picture-600.jpg`, and a post is created at `_posts/YYYY-MM-DD-cat-picture.markdown`.

Duplicate photos are skipped, and the script stops executing once it notices that all the pictures have already been downloaded.