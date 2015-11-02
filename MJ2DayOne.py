
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
	<date>2015-11-02T20:10:46Z</date>
	<key>Creator</key>
	<dict>
		<key>Device Agent</key>
		<string>Macintosh/MacBookAir6,2</string>
		<key>Generation Date</key>
		<date>2015-11-02T20:10:46Z</date>
		<key>Host Name</key>
		<string>armor.lanl.gov</string>
		<key>OS Agent</key>
		<string>MacOS/10.10.5</string>
		<key>Software Agent</key>
		<string>Day One Mac/1.10.1</string>
	</dict>
	<key>Entry Text</key>
	<string>This is a test. I want to know what happens if I do this here.</string>
	<key>Location</key>
	<dict>
		<key>Administrative Area</key>
		<string>NY</string>
		<key>Country</key>
		<string>United States</string>
		<key>Latitude</key>
		<real>40.870095114862877</real>
		<key>Locality</key>
		<string>Brookhaven</string>
		<key>Longitude</key>
		<real>-72.884910881110642</real>
		<key>Place Name</key>
		<string>Brookhaven National Laboratory</string>
	</dict>
	<key>Starred</key>
	<false/>
	<key>Tags</key>
	<array/>
	<key>Time Zone</key>
	<string>America/New_York</string>
	<key>UUID</key>
	<string>A7BADD177A0544369B8FF0C8C216C8CA</string>
</dict>
</plist>
"""
if __name__ == "__main__":
    print("\nI'm converting from MacJournal to DayOne.\n")

    import argparse

    parser = argparse.ArgumentParser(description="Extract Macjournal data")
    parser.add_argument('mjdoc', nargs='+', type=str,
        help='MacJournal document location.')
    parser.add_argument('--xml', type=str, default=None,
        help='Write XML file for human readability')

    args = parser.parse_args()

#   mjDoc = MJParser.mjdoc(args.mjdoc[0], verbose=True)

#   if args.xml:
#       mjDoc.MakeXMLFile(args.xml)
