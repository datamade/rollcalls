from backports import csv
import codecs
import sys
import locale
import collections

reader = csv.reader(codecs.getreader(locale.getpreferredencoding())(sys.stdin))
next(reader)

votes = collections.defaultdict(dict)
legislators = set()

for bill_id, name, vote, motion in reader :
    if name :
        votes[bill_id, motion][name] = vote
        legislators.add(name)


        
sort_key = lambda x : (x.split(',')[-1], x)

writer = csv.DictWriter(codecs.getwriter(locale.getpreferredencoding())(sys.stdout),
                        ['bill_id', 'motion'] + sorted(legislators, key=sort_key) + ['yes', 'no', 'margin'])
writer.writeheader()

for (bill_id, motion), voters in votes.items() :
    yes = sum(1 for vote in voters.values() if vote == 'yes')
    no = sum(1 for vote in voters.values() if vote == 'no')
    margin = yes - no
    voters['bill_id'], voters['motion'] = bill_id, motion
    voters['yes'], voters['no'], voters['margin'] = yes, no, margin
    writer.writerow(voters)
