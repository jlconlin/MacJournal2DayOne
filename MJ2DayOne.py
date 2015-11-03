
from __future__ import print_function

import os
import subprocess
import sys
sys.path.append("parser")

import pypandoc

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
	<string>{entryText}</string>
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
	<string>{id}</string>
</dict>
</plist>
"""

def entryData(Entry, mjDoc):
    """
    entryData will return a dictionary that contains the meta data used to
    create a Day One entry. The meta data comes from the MacJournal entry: Entry.
    """
    metaData = {}

    generator =  mjDoc.macjournalml.getElementsByTagName('generator')[0]
    metaData['agentVersion'] = generator.getAttribute('version')

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

    # ID---remove '-' from MacJournal ID
    metaData['id'] = Entry.content['id'].replace('-','')

    return metaData

def entryText(Entry, mjDoc, format="txt"):
    """
    entryText will extract the text for the entry. It returns the text as a
    string.

    format: The format to which you want the entry text formatted.
    """
    filename = os.path.join(mjDoc.Content, Entry.filename)

    # Copy file to cwd. I don't know why Python can't otherwise find the file.
    os.system( 'cp "{}" .'.format(filename) )

    # Convert the file to preferred format
    cmd = 'textutil -convert {} "{}" -stdout'.format(format, Entry.filename)
    content = subprocess.check_output(cmd, shell=True)

    # Delete copied file
    os.system( 'rm "{}"'.format(Entry.filename) )

    return content

def makeJournal(path):
    """
    makeJournal will create the directories needed in which the entries will be
    stored.
    """
    if not os.path.exists(journalPath):
        os.makedirs( os.path.join(journalPath, "entries") )
        os.makedirs( os.path.join(journalPath, "photos") )

def makeEntries(journalPath, Entries):
    """
    """
    pass

if __name__ == "__main__":
    print("\nI'm converting from MacJournal to DayOne.\n")

    import argparse

    parser = argparse.ArgumentParser(description="Extract Macjournal data")
    parser.add_argument('mjdoc', nargs='+', type=str,
        help='MacJournal document location.')
    parser.add_argument('--xml', type=str, default=None,
        help='Write XML file for human readability')
    parser.add_argument('--format', type=str, default="txt",
        help='Format to which the entry text will be converted')

    parser.add_argument('--journal-name', type=str, default="Journal",
        help="Name of DayOne journal file; '.dayone' will be appended.")

    args = parser.parse_args()

#   mjDoc = MJParser.mjdoc(args.mjdoc[0], verbose=True)

    if args.xml:
        mjDoc.MakeXMLFile(args.xml)

    mjEntry = mjDoc.Journals['Daily Journal'].Journals['2015'].Entries[0]
    metaData = entryData(mjEntry, mjDoc)
    metaData['entryText'] = entryText(mjEntry, mjDoc, format=args.format)

    journalPath = "{}.dayone".format(args.journal_name)
    makeJournal(journalPath)




