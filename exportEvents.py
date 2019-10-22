"""
Fetch all events for a given issue
You need to create an API KEY from Sentry before using this script
Regex to extract user email from user Object: ({u'username': None, u'name': None, u'ip_address': u'[0-9.]+', u'email': None, u'data': None, u'id': u')([^\W][a-zA-Z0-9_\-.]+(\.[a-zA-Z0-9_\-.]+)*\@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*\.[a-zA-Z]{2,4})('})
"""

import requests
import csv


def download_data(issue,token, outfile):
    with open(outfile, 'w') as csvfile:
        fieldnames = [u'eventID', u'user', u'dateCreated',u'platform', u'id', u'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        url = 'https://sentry.io/api/0/issues/{0}/events/'.format(issue)
        while True:
            response = requests.get(url, headers={'Authorization': 'Bearer {0}'.format(token)})
            data = response.json()
            for event in data:
                try:
                    writer.writerow(event)
                except:
                    print event
                    exit(1)
            link = response.headers.get('Link')
            if link and '"next"' in link:
                print("Getting next page...")
                url = link.split()[4][1:-2]
            else:
                break



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='download sentry as csv')

    parser.add_argument('-t', '--token', required=True)
    parser.add_argument('-i', '--issue', required=True)
    parser.add_argument('-f', '--file', required=False, default='out.csv')
    args = parser.parse_args()
    print "download csv for {0}".format(args.issue)
    download_data(args.issue, args.token, args.file)
