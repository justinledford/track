# track
Command line interface to track USPS and UPS shipments by tracking numbers, utilizing a web scraper to gather data. This was created for personal use, without the need to register for any API.


#### Usage

    usage: track.py [-h] [-l | -p PACKAGE_NAME]
  
    optional arguments:
      -h, --help       show this help message and exit
      -l               list packages in config, looks for
                       $HOME/.config/track/config.yaml
      -p PACKAGE_NAME  package to track
      -e               edit config file with $EDITOR or vi

#### Configuration Example
    USPS:
        1234567890: foobar


#### Dependencies
Python 3.5  
beautifulsoup4  
requests  
PyYAML  


#### To-do:

Support for additional carriers such as DHL, Dynamex, etc.
Option to list only most recent statuses for each package.  


