
# vim: set fileencoding=utf-8

from __future__ import print_function

import os
import subprocess
import sys
sys.path.append("parser")
import MJParser

dayOneBasicString = u"""
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
    <string>{entryText}
    </string>{location}
    <key>Starred</key>
    <false/>
    <key>Tags</key>
    <array>{tags}
    </array>
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

    generator = mjDoc.macjournalml.getElementsByTagName('generator')[0]
    metaData['agentVersion'] = generator.getAttribute('version')

    # Date
    fmt = "%Y-%m-%dT%H:%M:%S"
    metaData['date'] = "{}Z".format(Entry.date.strftime(fmt))

    # Location data
    metaData['timezone'] = Entry.timezone()
    location = Entry.location()
    if location:
        metaData['location'] = """
    <key>Location</key>
    <dict>
        <key>Latitude</key>
        <real>{latitude}</real>
        <key>Longitude</key>
        <real>{longitude}</real>
    </dict>\n""".format(latitude=location[0], longitude=location[1])
    else:
        metaData['location'] = ""

    # Tags
    keywords = Entry.keywords()
    tags = [" "*16 + u"<string>{}</string>".format(word) for word in keywords]
    metaData['tags'] = "\n" + "\n".join(tags)

    # ID---remove '-' from MacJournal ID
    metaData['id'] = Entry.content['id'].replace('-', '')

    return metaData


def entryText(Entry, mjDoc, format="txt"):
    """
    entryText will extract the text for the entry. It returns the text as a
    string.

    format: The format to which you want the entry text formatted.
    """
    filename = os.path.join(mjDoc.Content, Entry.filename)

    # Copy file to cwd.
    # I don't know why Python can't otherwise find the file.
    os.system('cp -r "{}" .'.format(filename))

    # Convert the file to preferred format
    if format == "txt":
        cmd = 'textutil -convert {} "{}" -stdout'.format(format, Entry.filename)
        content = subprocess.check_output(cmd, shell=True)

        # Convert to unicode (I hope)
        content = unicode(content, "utf-8")

        # Replace special characters
        content = content.replace('&', '&amp;')
        content = content.replace('<', '&lt;')
        content = content.replace('<', '&gt;')

    else:
        raise NotImplementedError(
            "I don't know how to convert to format: {}".format(format))

    # Delete copied file
    os.system('rm -rf "{}"'.format(Entry.filename))

    return content


def makeJournal(path):
    """
    makeJournal will create the directories needed in which the entries will be
    stored.
    """
    if not os.path.exists(journalPath):
        os.makedirs(os.path.join(journalPath, "entries"))
        os.makedirs(os.path.join(journalPath, "photos"))


def makeEntries(journalPath, mjDoc, Entries, format):
    """
    makeEntries will create a journal entry for each entry in Entries.
    Entries.
    """
    print("\nMaking entries for:")
    for i, entry in enumerate(Entries):
        print(u"\t{:4d}-{}".format(i, entry.name))
        metaData = entryData(entry, mjDoc)
        eText = entryText(entry, mjDoc, format=args.format)
        metaData['entryText'] = eText.replace('\t', '\n')

        filename = os.path.join(journalPath, "entries",
                                '{}.doentry'.format(metaData['id']))

        text = dayOneBasicString.format(**metaData)

        with open(filename, 'w') as entryFile:
            entryFile.write(text.encode("utf-8"))

    print("{} entries".format(i))


def extractEntries(journal):
    """
    extractEntries will collect all the entries in a journal and return them in
    a list. This will call recursively to all the nested journals.
    """
    print("Extracting entries from journal: {}".format(journal))
    entries = []

    # Add entries from current journal
    entries.extend(journal.Entries)

    # Add entries from all sub journals
    for subJournal in journal.Journals.values():
        entries.extend(extractEntries(subJournal))

    return entries


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

    parser.add_argument('--journal', type=str, default="Daily Journal",
        help='Name of MacJournal journal from which entries will be converted.')
    parser.add_argument('--journal-name', type=str, default="Journal",
        help="Name of DayOne journal file; '.dayone' will be appended.")

    args = parser.parse_args()

    mjDoc = MJParser.mjdoc(args.mjdoc[0], verbose=True)

    if args.xml:
        mjDoc.MakeXMLFile(args.xml)

    journalPath = "{}.dayone".format(args.journal_name)
    makeJournal(journalPath)

    Entries = extractEntries(mjDoc.Journals[args.journal])
    makeEntries(journalPath, mjDoc, Entries, args.format)

#   entry = Entries[2778]
#   metaData = entryData(entry, mjDoc)
#   metaData['entryText'] = entryText(entry, mjDoc, format="txt").replace('\t', '\n')
#   makeEntries(journalPath, mjDoc, [entry], args.format)
