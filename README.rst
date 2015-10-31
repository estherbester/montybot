MONTYBOT
########

Montybot is a human friendly IRC bot.  currently it supplies cute pictures of
animals to humans.

HOW TO USE
==========
* In the shell, run:

.. code-block::

    $ "python event.py "<channel>"

* To use Puppy Bot you need a Flickr API key. Currently the group used is corgis but you can change that, obviously (though why would you want to?)

REQUIREMENTS
============

* headers (``apt-get install python-dev``)

* `Twisted and its dependencies <https://twistedmatrix.com/trac/>`_
* `flickrpy <https://code.google.com/p/flickrpy/>`_
* `python-requests <http://docs.python-requests.org/en/latest/>`_
* `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_

For PuppyBot

    * flickrpy (included here as flickr.py because I patched it slightly; source https://code.google.com/p/flickrpy/)
    * flickr API key (store in secret_settings.py as API_KEY and API_SECRET; see SAMPLE file included here)

For Link log

    * python-requests [python-requests.org]
    * BeautifulSoup
    * Create an empty text file, called 'links_in_channel.txt', in the same directory as the app.


THANKS TO
=========
* bmessemer for invaluable feedback

