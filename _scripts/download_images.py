import requests
import re
from urlparse import urlparse
import urllib
import os
import codecs

POSTS_PATH = '/home/zan/websites/mymusings/_posts/'
PATHS = os.listdir(POSTS_PATH)

IMAGE_REGEX = "!\[.*?\]\((?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\)"

def download_and_save(url, path=None):
    r = requests.get(url, stream=True)
    if not path:
        path = get_path(url)
        path = '/img/' + path
    save_path = '/home/zan/websites/mymusings' + path
    if r.status_code == 200:
        try:
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
                print "Successfully saved image %s" % path
        except Exception as e:
            print "Error in saving image %s: %s" % (url, e)
            return False
        return True
    else:
        return False

def get_path(url, safe=True):
    url_obj = urlparse(url)
    path = url_obj.path
    if safe:
        path = urllib.quote(path, '')
    path = path.replace('%', '')
    return path

def sub_image(matchobj):
    print "Starting to migrate image %s" % matchobj.group()
    url = matchobj.group('url')
    path = '/img/' + get_path(url)
    is_saved = download_and_save(url, path)
    # is_saved = True
    if is_saved:
        new_path = '![](' + path + ')'
        print "Changing path to %s" % new_path
        return new_path
    else:
        print "Not changing anything"
        return matchobj.group()

def main():
    print "Starting"
    for post_path in PATHS:
        print "Opening post %s" % post_path
        with open(POSTS_PATH + post_path, 'r') as f:
            post = f.read()
            post = post.replace('\n', ' ')
        (new_post, count) = re.subn(IMAGE_REGEX, sub_image, post, re.M)
        if count > 0:
            with codecs.open(POSTS_PATH + post_path, 'w', 'utf-8') as f:
                f.write(unicode(new_post, 'utf-8'))
                print 'Successfully wrote %s' % post_path
        print "Migrated %d images" % count
    print "Finished!"

if __name__ == '__main__':
    main()