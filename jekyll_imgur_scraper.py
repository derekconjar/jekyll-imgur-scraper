import urllib
import re
import sys
import datetime
import os.path

from imgurpython import ImgurClient
from PIL import Image, ImageOps

client_id = 'API_CLIENT_ID'
client_secret = 'API_CLIENT_SECRET'
client = ImgurClient(client_id, client_secret)

print("You're connected to the Imgur API.")

subreddit = str(raw_input('What subreddit should we scrape? '))
page_num = int(raw_input('What page number should we start at? '))
still_needs_to_be_processed = True

def generate_markdown(title, slug, image_filename):
    md =  '---\n'
    md += 'layout: post\n'
    md += 'title: "{}"\n'.format(title.replace('"','\\"'))
    md += 'image: "{}"\n'.format(image_filename)
    md +=  '---\n\n'

    now = datetime.datetime.now()
    month = '%02d' % now.month
    day = '%02d' % now.day
    datestr = '{0}-{1}-{2}'.format(now.year, month, day)

    md_filename = '_posts/{0}-{1}.markdown'.format(datestr, slug)
    md_file = open(md_filename, 'w')
    md_file.write(md)
    md_file.close()

    print(md_filename)

def generate_thumb(image_filename):
    size = (300,300)
    filepath = 'downloads/{}'.format(image_filename)
    thumb_filepath = 'thumbs/{}'.format(image_filename)

    try:
        image = Image.open(filepath)
    except:
        print('Unable to open image.')

    thumb = ImageOps.fit(image, size, Image.ANTIALIAS)
    thumb.save(thumb_filepath)

while still_needs_to_be_processed:
    items = client.subreddit_gallery(subreddit, window='all',
            page=page_num)
    dupes = 0

    print('Loading the items on page {}...'.format(page_num))

    for item in items:
        title = item.title.encode('utf-8')

        print('Processing "{}"...'.format(title))
        print("We're on page {}, BTW").format(page_num)

        image_source = item.link
        image_width = item.width
        image_height = item.height
        imgur_score = item.score

        slug = title.lower().replace(' ', '-')
        slug = re.sub(r'[^a-zA-Z0-9-_]', '', slug).split('-')

        if len(slug) > 6:
            slug = slug[0:6]

        slug = '-'.join(slug)

        image_file_ext = image_source.split('.')[-1]
        image_filename = slug + '-' + str(image_width) + '.' + image_file_ext
        image_filepath = 'downloads/{}'.format(image_filename)

        print('Checking if {} already exists...'.format(image_filename))

        if os.path.exists(image_filepath):
            print('This image has already been processed...')
            dupes += 1
        else:
            print('Downloading image to {}'.format(image_filepath))
            image_file = urllib.URLopener()

            try:
                image_file.retrieve(image_source, image_filepath)
            except:
                print('Seems to be an issue with downloading the image...')
                print('Moving on...')
                continue

            print('The image has been saved!')
            print('Now generating the thumbnail...')

            try:
                generate_thumb(image_filename)
            except:
                print('Unable to generate the thumbnail!')
                continue

            print('Now adding the markdown file...')

            try:
                generate_markdown(title, slug, image_filename)
            except:
                print('Problem generating the markdown!')
                continue

            print('Success!')
            print('Moving on to the next image...')

        if dupes > 5:
            print("I think we're done processing!")
            print('Later gator.')
            sys.exit()

    page_num += 1

    print("That's it for this page...")
    print('Moving on to page {}'.format(page_num))
