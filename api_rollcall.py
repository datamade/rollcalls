from sunlight import openstates
from backports import csv
from io import open

this_term = openstates.bills(state='il',
                             chamber='upper',
                             type='bill',
                             search_window='term')

votes = {}

for bill_slug in this_term :
    bill = openstates.bill(bill_slug['id'])
    if bill['action_dates']['passed_upper'] :
        bill_id = bill['bill_id']
        votes[bill_id] = {}
        last_vote = [vote for vote in bill['votes']
                     if vote['chamber'] == 'upper'][-1]
        vote_groups = (('yes', last_vote['yes_votes']),
                       ('no', last_vote['no_votes']),
                       ('other', last_vote['other_votes']))
        
        for response, legislators in vote_groups :
            for legislator in legislators :
                votes[bill_id][legislator['name']] = response

legislators = set()
for bill_vote in votes.values() :
    legislators.update(bill_vote.keys())

with open('rollcall.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, ['bill_id'] + list(legislators))
    writer.writeheader()
    for bill_id, bill_vote in votes.items() :
        bill_vote['bill_id'] = bill_id
        writer.writerow(bill_vote)
    
