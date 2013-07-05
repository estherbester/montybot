import flickr
from random import randint
from random import choice

from secret_settings import API_KEY
from secret_settings import API_SECRET

flickr.API_KEY = API_KEY
flickr.API_SECRET = API_SECRET
photos_per_page = 2

# Need the NSID of whatever group you're pulling from
GROUPS = {
    'corgi': '42653350@N00',
    'pug': '57017533@N00',
    'doxy': '52240151476@N01',
    'puppy': '35034344814@N01'
}


def get_puppy(group):
        group = flickr.Group(GROUPS.get(group, GROUPS['puppy']))
        photos = None
        counter = 1
        while photos is None and counter < 3:
            try:
                # Trying to randomize the fetch a bit, limited by the number of photos in the group
                random_page = randint(1, group.poolcount / photos_per_page)
                photos = group.getPhotos(per_page=photos_per_page,
                                         page=random_page)
                # More randomizing
                one_photo = choice(photos)
            except (AttributeError, flickr.FlickrError) as e:
                print "Error: %s" % e
                counter += 1
        # This could be better
        if photos is None:
            # Since we failed at randomizing just get one from the first page of results
            print "Randomized fetching failed. Getting one from the front page"
            photos = group.getPhotos(per_page=100, page=1)
            one_photo = choice(photos)
        try:
            return get_photo_url(one_photo)
        except flickr.FlickrError:
            return "Sorry, no puppy for you =("


def get_photo_url(photo, size="Medium"):
    method = 'flickr.photos.getSizes'
    data = flickr._doget(method, photo_id=photo.id)
    return _get_resized(data, size)
    raise flickr.FlickrError, "No URL found"


def _get_resized(data, size):
    for psize in data.rsp.sizes.size:
        if psize.label == size:
            return psize.source

if __name__ == '__main__':
    import sys
    try:
        group = sys.argv[1]
        print get_puppy(group)
    except IndexError:
        print "Please specify a group"
