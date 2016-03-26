from backports import csv
import codecs
import sys
import locale
import collections

reader = csv.reader(codecs.getreader(locale.getpreferredencoding())(sys.stdin))
next(reader)

votes = collections.defaultdict(dict)
legislators = set()

for bill_id, name, vote in reader :
    votes[bill_id][name] = vote
    legislators.add(name)


writer = csv.DictWriter(codecs.getwriter(locale.getpreferredencoding())(sys.stdout),
                        ['bill_id'] + sorted(legislators))
writer.writeheader()

for bill_id, voters in votes.items() :
    voters['bill_id'] = bill_id
    writer.writerow(voters)
