from applicants.models import Achievement
import datetime


def dump_csv(option):
    fields = [ 'reviewer_id', 'user_id', 'org_address', 'org_phone', 'org_email', 'research_goal', 'relevance',
               'expected_results', 'authors']
    reviewed = Achievement.objects.filter(applicationvote__approved=option).prefetch_related(
        'applicationvote_set', 'author_set').order_by('-sent')
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
            voted_by = inst.applicationvote_set.first().reviewer
            file.write(f'{voted_by},{inst.user},{inst.csv_representation()},{authors_csv}\n')
    return filename
