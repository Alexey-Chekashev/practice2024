from applicants.models import Achievement
import datetime
import csv
from applicants.models import Author
from reviewers.models import ApplicationVote


# def dump_csv2(option):
#     fields = [ 'reviewer_id', 'user_id', 'org_address', 'org_phone', 'org_email', 'research_goal', 'relevance',
#                'expected_results', 'authors']
#     reviewed = Achievement.objects.filter(applicationvote__approved=option).prefetch_related(
#         'applicationvote_set', 'author_set').order_by('-sent')
#     option = "approved" if option else "rejected"
#     filename = f"csvs\\{option}_achievements_{str(datetime.datetime.now()).replace(':', '_')}.csv"
#     before = time.perf_counter_ns()
#     with open(filename, 'w+') as file:
#         file.write(','.join(fields)+'\n')
#         for inst in reviewed:
#             authors = inst.author_set.all().order_by('order_number')
#             authors_csv = '"'
#             for author in authors:
#                 authors_csv = authors_csv + author.csv_representation() + ","
#             authors_csv = authors_csv[:-1] + '"'
#             voted_by = inst.applicationvote_set.first().reviewer.id
#             file.write(f'"{voted_by}",{inst.csv_representation()},{authors_csv}\n')
#     print(time.perf_counter_ns() - before)
#     return filename


def dump_csv(option):
    fields = ['user','org_address','org_phone','org_email','research_goal', 'relevance','expected_results', 'created']
    reviewed = Achievement.objects.filter(applicationvote__approved=option).order_by('-sent').values_list(*(['id']+fields))
    option = "approved" if option else "rejected"
    filename = f"csvs\\test_{option}_achievements_{str(datetime.datetime.now()).replace(':', '_')}.csv"
    # before = time.perf_counter_ns()
    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file, delimiter='|', quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer.writerow(['reviewer_id'] + ['user_id'] + fields[1:] + ['authors'])
        for inst in reviewed:
            inst_id = inst[0]
            inst_new = inst[1:]
            authors = Author.objects.filter(achievement=inst_id).order_by('order_number').values_list(*['last_name', 'first_name', 'middle_name'])
            authors_csv = ''
            for author in authors:
                authors_csv = authors_csv + '"' + ','.join(author) + '"' + ','
            authors_csv = [authors_csv[:-1]]
            voted_by = [str(ApplicationVote.objects.get(application=inst_id).reviewer_id)]
            writer.writerow(voted_by+list(inst_new)+authors_csv)
    # print(time.perf_counter_ns() - before)
    return filename

