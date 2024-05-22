from applicants.models import Achievement
import datetime
import csv


def dump_csv(option):
    fields = [ 'voted_user', 'user', 'org_address', 'org_phone', 'org_email', 'research_goal', 'relevance', 'expected_results',
              'authors']
    reviewed = Achievement.objects.filter(applicationvote__approved=option).prefetch_related(
        'applicationvote_set', 'author_set').order_by('-sent').select_related('user')
    option = "approved" if option else "rejected"
    filename = f"csvs\\{option}_achievements_{str(datetime.datetime.now()).replace(':', '_')}.csv"
    with open(filename, 'w+') as file:
        file.write(','.join(fields)+'\n')
        for inst in reviewed:
            authors = inst.author_set.all().order_by('order_number')
            authors_csv = '"'
            for author in authors:
                authors_csv = authors_csv + author.csv_representation() + ","
            authors_csv = authors_csv[:-1] + '"'
            vote = inst.applicationvote_set.first()
            voted_by = vote.reviewer.username
            inst_csv = f"{inst.org_address},{inst.org_phone},{inst.org_email},{inst.research_goal},{inst.relevance},{inst.expected_results}"
            file.write(voted_by + ',' + inst.user.username + ',' + inst_csv + ',' + authors_csv + '\n')
    return filename
