
from __future__ import print_function

import sys
sys.path.append("parser")

import MJParser

dayOneBasicString = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Creation Date</key>
	<date>{date}</date>
	<key>Creator</key>
	<dict>
		<key>Generation Date</key>
		<date>{date}</date>
		<key>Software Agent</key>
		<string>MacJournal/{agentVersion}</string>
	</dict>
	<key>Entry Text</key>
	<string>This is a test. I want to know what happens if I do this here.</string>
	<key>Location</key>
	<dict>
		<key>Latitude</key>
		<real>{latitude}</real>
		<key>Longitude</key>
		<real>{longitude}</real>
	</dict>
	<key>Starred</key>
	<false/>
	<key>Tags</key>
	<array>{tags}</array>
	<key>Time Zone</key>
	<string>{timezone}</string>
	<key>UUID</key>
	<string>A7BADD177A0544369B8FF0C8C216C8CA</string>
</dict>
</plist>
"""

def entryData(Entry):
    """
    entryData will return a dictionary that contains the meta data used to
    create a Day One entry. The meta data comes from the MacJournal entry: Entry.
    """
    metaData = {}

    # Date
    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    metaData['date'] = "{}Z".format( Entry.date.strftime(fmt) )

    # Location data
    metaData['timezone'] = Entry.timezone()
    metaData['latitude'] = Entry.latitude()
    metaData['longitude'] = Entry.latitude()

    # Tags
    keywords = Entry.keywords()
    tags = [" "*8 + "<string>{}</string>\n".format(word) for word in keywords]
    metaData['tags'] = tags

    return metaData

if __name__ == "__main__":
    print("\nI'm converting from MacJournal to DayOne.\n")

    import argparse

    parser = argparse.ArgumentParser(description="Extract Macjournal data")
    parser.add_argument('mjdoc', nargs='+', type=str,
        help='MacJournal document location.')
    parser.add_argument('--xml', type=str, default=None,
        help='Write XML file for human readability')

    args = parser.parse_args()

    mjDoc = MJParser.mjdoc(args.mjdoc[0], verbose=True)

    if args.xml:
        mjDoc.MakeXMLFile(args.xml)

    # Find some global data for string formatting
    mjArgs = {}
    generator =  mjDoc.macjournalml.getElementsByTagName('generator')[0]
    mjArgs['agentVersion'] = generator.getAttribute('version')

