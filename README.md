# track
Command line interface to track shipments

Currently supports USPS tracking numbers.
  
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

Support for tracking UPS and FedEx shipments.
