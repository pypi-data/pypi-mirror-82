sp\_yt\_search
==============

Parse Spotify URI to Youtube link

Installation
~~~~~~~~~~~~

Just use (No other package is needed):

.. code:: sh

    $ pip install sp_yt_search

Example Usage
~~~~~~~~~~~~~

.. code:: python

    from sp_yt_search import SpYt


    if __name__ == '__main__':
        # Setup credentials
        client_id = 'spotify_api_client_id'
        secret = 'spotify_api_secret'
        # Provide Spotify URI
        uri = 'spotify:track:4uLU6hMCjMI75M1A2tKUQC'

        sp = SpYt()                             # Initialize SpYt object
        sp.set_credentials(client_id, secret)   # Auth Spotify

        sp.sp_search(uri)                       # Search for URI
        print(sp.get_data())                    # Prints found spotify objects

        sp.yt_search()                          # Perform YT search for found Spotify objects
        print(sp.get_data())                    # Prints spotify objects with YouTube related results

Availible URIs
~~~~~~~~~~~~~~

Package can be used for fetching:

-  Track:

   ::

       spotify:track:{ID}

-  Playlist:

   ::

       spotify:playlist:{ID}

-  Album:

   ::

       spotify:album:{ID}

-  Artist:

   ::

       spotify:artist:{id}}

See me on `github <https://github.com/MarcinMysliwiec>`__

License MIT
~~~~~~~~~~~

**Free Software, Hell Yeah!**
