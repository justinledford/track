#!/usr/bin/python3

import argparse
from collections import OrderedDict
from datetime import datetime
import os
import subprocess
import sys

from bs4 import BeautifulSoup
import requests
import yaml

CONFIG_PATH = "{}/.config/track/config.yaml".format(os.environ['HOME'])

def main():
    parser = argparse.ArgumentParser()
    exclusive_args = parser.add_mutually_exclusive_group()
    exclusive_args.add_argument('-l', action='store_true',
                                help="list packages in config, looks for \
                                        $HOME/.config/track/config.yaml")
    exclusive_args.add_argument('-p', metavar="PACKAGE_NAME", 
                                action="store",
                                help='package to track')
    exclusive_args.add_argument('-e', action='store_true',
                                help='edit config file with $EDITOR or vi')
    args = parser.parse_args()

    if args.l:
        list_packages()
    if args.p:
        track_package(args.p)
    if args.e:
        edit_config()
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)


# Remove whitespace in USPS strings
def remove_whitespace(s):
    return s.replace('\r', '').replace('\t','').replace('\n','')


# Fix USPS datetime formatting
def fix_usps_datetime(date_time):
    s = date_time.split(",")
    if len(s) == 2:
        # In case no time is given
        return "{}, {}".format(s[0], s[1].lstrip())
    else:
        return "{}, {}, {}".format(s[0], s[1].lstrip(), s[2])


# Make request and return OrderedDict of status updates
def get_usps_data(tracking_number):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/34.0.1847.131 Safari/537.36'
    url = "https://tools.usps.com/go/TrackConfirmAction?qtc_tLabels1="\
            + tracking_number
    headers = {'user-agent': user_agent}
    r = requests.get(url, headers=headers)
    
    html = r.text

    # There is a missing </p> tag in the first "status"
    # <td>, causing BeautifulSoup to ignore the parent
    # <td>, removing all <p> and </p> tags fixes this issue
    html = html.replace('<p>','').replace('</p>','')

    soup = BeautifulSoup(html, 'html.parser')
    table_rows = soup.find_all("tr", class_="detail-wrapper")

    if not table_rows:
        return None

    data = {}
    for tr in table_rows:
        date_time_td = tr.find("td", class_="date-time")
        date_time = remove_whitespace(date_time_td.string)
        date_time = fix_usps_datetime(date_time)
        try:
            timestamp = datetime.strptime(date_time,
                    "%B %d, %Y, %I:%M %p").timestamp()
        except:
            timestamp = datetime.strptime(date_time,
                    "%B %d, %Y").timestamp()


        status_td = tr.find("td", class_="status")
        status_p = status_td.find("p")

        # Some status strings are in an additional span child
        if "clearfix" in status_p["class"]:
            status_span = status_p.find("span")
            status = remove_whitespace(status_span.string.lstrip())
        else:
            # There is an <input> along with text in
            # this element, get just the text.
            status = remove_whitespace(status_p.contents[0])

        location_td = tr.find("td", class_="location")
        location = remove_whitespace(location_td.string)

        data[timestamp] = {}
        data[timestamp]["date_time"] = date_time
        data[timestamp]["status"] = status
        data[timestamp]["location"] = location

    return OrderedDict(sorted(data.items()))


def print_history(history):
    for a, b in history.items():
        print(b['date_time'])
        print('\t' + b['status'])
        print('\t' + b['location'])


def list_packages():
    config = yaml.load(open(CONFIG_PATH, 'r'), Loader=yaml.BaseLoader)

    for carrier, shipments in config.items():
        print(carrier)
        for number, name in shipments.items():
            print("\t{}: {}".format(name, number))


def track_package(package_name):
    config = yaml.load(open(CONFIG_PATH, 'r'), Loader=yaml.BaseLoader)

    for carrier, shipments in config.items():
        for number, name in shipments.items():
            if package_name == name:
                tracking_number = number
                break

    try:
        history = get_usps_data(tracking_number)
        print_history(history)
    except:
        print("Tracking information not found")


def edit_config():
    try:
        subprocess.run([os.environ['EDITOR'], CONFIG_PATH])
    except:
        subprocess.run(["vi", CONFIG_PATH])

if __name__ == "__main__":
    main()
