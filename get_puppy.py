import flickr
from random import randint
from random import choice 

from secret_settings import API_KEY
from secret_settings import API_SECRET

flickr.API_KEY = API_KEY
flickr.API_SECRET = API_SECRET

# Need the NSID of whatever group you're pulling from
FLICKR_GROUP = '42653350@N00' # corgi
PUG_GROUP = '57017533@N00'  # pug


def get_puppy(group_id):
        group = flickr.Group(group_id)
        photos = None
        counter = 1
        while photos is None and counter < 3:
            try:
                # Trying to randomize the fetch a bit, limited by the number of photos in the group
                random_page = randint(1, group.poolcount)
                photos = group.getPhotos(per_page=2, page=random_page)
                # More randomizing
                one_photo = random.choice(photos) 
            except AttributeError, flickr.FlickrError:
                counter += 1
        # This could be better
        if photos is None:
            # Since we failed at randomizing just get one from the first page of results
            print "Getting one from the front page"
            photos = group.getPhotos(per_page=100, page=1)
            one_photo = random.choice(photos)
        try:
            return get_photo_url(one_photo)
        except flickr.FlickrError:
            return "Sorry, no puppy for you =("


def get_photo_url(photo, size="Medium"):
    method = 'flickr.photos.getSizes'
    data = flickr._doget(method, photo_id=photo.id)
    for psize in data.rsp.sizes.size:
        if psize.label == size:
            return psize.source
    raise flickr.FlickrError, "No URL found"

if __name__ == '__main__':
    print get_puppy(PUG_GROUP)
