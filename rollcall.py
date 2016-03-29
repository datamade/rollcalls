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
    if name :
        votes[bill_id][name] = vote
        legislators.add(name)

sort_key = lambda x : (x.split(',')[-1], x)

writer = csv.DictWriter(codecs.getwriter(locale.getpreferredencoding())(sys.stdout),
                        ['bill_id'] + sorted(legislators, key=sort_key))
writer.writeheader()

for bill_id, voters in votes.items() :
    voters['bill_id'] = bill_id
    writer.writerow(voters)
