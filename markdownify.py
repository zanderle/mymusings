from html2text import html2text as h2t
import os
import codecs


# loop through _posts/
path_to_posts = '/home/zan/websites/mymusings/_posts/'
path_to_migrate = path_to_posts + 'md/'
html_files = os.listdir(path_to_posts)
html_files = [h for h in html_files if h != 'md']

print('Starting to migrate posts')

for html_file in html_files:
    print('Migrating %s' % html_file)
    front_matter = None
    md = None
    with open(path_to_posts + html_file, 'r') as f:
        print('Reading file...')
        raw = f.read()
# copy front-matter
        index = raw.find('---', 3)  # look for '---' but only after the beginning
        if index == -1 or index == 0:
            raise Exception
        # From where to where?
        front_matter = raw[:index+3]
# take the rest (which should be html) and run it through html2text
        html = raw[index+3:]
        md = h2t(unicode(html, 'utf-8'))

# save to file in _posts/migrate/_.md
    if md and front_matter:
        md_file = html_file[:-4] + 'md'
        with codecs.open(path_to_migrate + md_file, 'w', 'utf-8') as f:
            f.write(front_matter)
            f.write('\n')
            f.write(md)
            print('Successfully migrated %s' % html_file)