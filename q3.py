import csv
import multiprocessing
from datetime import datetime


def find_site_with_largest_number_of_unique_user(country_id):
    unique_user_ids_by_site_id = {}
    site_ids_with_largest_users = []
    sites_with_largest_users = []
    with open("sample_data_q3.csv", 'r') as csvfile:
        site_access_logs = csv.DictReader(csvfile)
        for access in site_access_logs:
            if country_id == access['country_id']:
                if access['site_id'] not in unique_user_ids_by_site_id.keys():
                    unique_user_ids_by_site_id[access['site_id']] = []

                unique_user_ids_by_site_id[access['site_id']].append(access['user_id'])
                unique_user_ids_by_site_id[access['site_id']] = list(set(unique_user_ids_by_site_id[access['site_id']]))
                if not site_ids_with_largest_users:
                    site_ids_with_largest_users.append(access['site_id'])
                    sites_with_largest_users.append({
                        'site_id': access['site_id'],
                        'number_of_unique_users': len(unique_user_ids_by_site_id[access['site_id']])
                    })
                else:
                    if len(unique_user_ids_by_site_id[access['site_id']]) > len(unique_user_ids_by_site_id[site_ids_with_largest_users[0]]):
                        site_ids_with_largest_users.clear()
                        sites_with_largest_users.clear()
                        site_ids_with_largest_users.append(access['site_id'])
                        sites_with_largest_users.append({
                            'site_id': access['site_id'],
                            'number_of_unique_users': len(
                                unique_user_ids_by_site_id[access['site_id']])
                        })
                    elif len(unique_user_ids_by_site_id[access['site_id']]) == len(unique_user_ids_by_site_id[site_ids_with_largest_users[0]]):
                        if access['site_id'] not in site_ids_with_largest_users:
                            site_ids_with_largest_users.append(access['site_id'])
                            sites_with_largest_users.append({
                                'site_id': access['site_id'],
                                'number_of_unique_users': len(
                                    unique_user_ids_by_site_id[access['site_id']])
                            })
                        else:
                            sites_with_largest_users[
                                site_ids_with_largest_users.index(access['site_id'])].update({
                                'site_id': access['site_id'],
                                'number_of_unique_users': len(
                                    unique_user_ids_by_site_id[access['site_id']])
                            })

    csvfile.close()
    return sites_with_largest_users


def find_site_visitors(min_visit_num_per_site, start_datetime, end_datetime):
    start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')

    with open("sample_data_q3.csv", 'r') as csvfile:
        site_access_logs = csv.DictReader(csvfile)

        sites_visited_by_user = {}
        visiters_with_more_than_min_visit = {}
        for access in site_access_logs:
            access_datetime = datetime.strptime(access['ts'], '%Y-%m-%d %H:%M:%S')
            if start_datetime <= access_datetime <= end_datetime:
                if access['user_id'] not in sites_visited_by_user.keys():
                    sites_visited_by_user[access['user_id']] = {}
                if access['site_id'] not in sites_visited_by_user[access['user_id']].keys():
                    sites_visited_by_user[access['user_id']][access['site_id']] = 0
                sites_visited_by_user[access['user_id']][access['site_id']] = \
                sites_visited_by_user[access['user_id']][access['site_id']] + 1
                if sites_visited_by_user[access['user_id']][
                    access['site_id']] >= min_visit_num_per_site:
                    visiters_with_more_than_min_visit[access['user_id']] = (
                        access['user_id'],
                        access['site_id'],
                        sites_visited_by_user[access['user_id']][access['site_id']]
                    )
    csvfile.close()
    return [visiters_with_more_than_min_visit[user_id] for user_id in
            visiters_with_more_than_min_visit]


def find_top_sites_visited_last_time():
    datetime_format = '%Y-%m-%d %H:%M:%S'
    access_datetimes_by_user = {}
    visited_sites_by_user_id_datetime = {}
    num_of_users_by_visited_site = {}

    with open("sample_data_q3.csv", 'r') as csvfile:
        site_access_logs = csv.DictReader(csvfile)

        for access in site_access_logs:
            access_datetimes_by_user \
                .setdefault(access['user_id'], []) \
                .append(datetime.strptime(access['ts'], datetime_format))
            visited_sites_by_user_id_datetime \
                .setdefault('{}_{}'.format(access['user_id'], access['ts']), access['site_id'])
            num_of_users_by_visited_site.setdefault(access['site_id'], 0)

        for user_id in access_datetimes_by_user:
            last_datetime_str = sorted(access_datetimes_by_user[user_id],
                                       reverse=True)[0].strftime(datetime_format)
            if '{}_{}'.format(user_id, last_datetime_str) in visited_sites_by_user_id_datetime.keys():
                site_id = visited_sites_by_user_id_datetime['{}_{}'.format(user_id, last_datetime_str)]
                num_of_users_by_visited_site[site_id] = num_of_users_by_visited_site[site_id] + 1

    top_visited_sites = sorted(num_of_users_by_visited_site.items(),
                               key=lambda kv: (kv[1], kv[0]),
                               reverse=True)
    csvfile.close()
    return top_visited_sites[:3]


def find_users_with_same_first_last_visit_sites():
    datetime_format = '%Y-%m-%d %H:%M:%S'
    access_datetimes_by_user = {}
    visited_sites_by_user_id_datetime = {}
    num_of_users_first_last_visit_same = 0

    with open("sample_data_q3.csv", 'r') as csvfile:
        site_access_logs = csv.DictReader(csvfile)

        for access in site_access_logs:
            access_datetimes_by_user \
                .setdefault(access['user_id'], []) \
                .append(datetime.strptime(access['ts'], datetime_format))
            visited_sites_by_user_id_datetime \
                .setdefault('{}_{}'.format(access['user_id'], access['ts']), access['site_id'])

        for user_id in access_datetimes_by_user:
            first_datetime_str = sorted(access_datetimes_by_user[user_id])[0]\
                                        .strftime(datetime_format)
            last_datetime_str = sorted(access_datetimes_by_user[user_id],
                                       reverse=True)[0].strftime(datetime_format)
            if '{}_{}'.format(user_id, first_datetime_str) in visited_sites_by_user_id_datetime.keys() \
                    and '{}_{}'.format(user_id, last_datetime_str) in visited_sites_by_user_id_datetime.keys():
                first_site_id = visited_sites_by_user_id_datetime['{}_{}'.format(user_id, first_datetime_str)]
                last_site_id = visited_sites_by_user_id_datetime['{}_{}'.format(user_id, last_datetime_str)]
                if first_site_id == last_site_id:
                    num_of_users_first_last_visit_same = num_of_users_first_last_visit_same + 1

    return num_of_users_first_last_visit_same


if __name__ == '__main__':
    # Test Question 3: Analytics
    """
        CASE 1
        Consider only the rows with country_id = "BDV" (there are 844 such rows).
        For each site_id, we can compute the number of unique user_id's found in these 844 rows.
        Which site_id has the largest number of unique users? And what's the number?
    """
    print('Site_with_largest_number_of_unique_user with country_id = BDV:')
    print(find_site_with_largest_number_of_unique_user(country_id='BDV'))
    print('')

    """
        CASE 2
        Between 2019-02-03 00:00:00 and 2019-02-04 23:59:59, 
        there are four users who visited a certain site more than 10 times. 
        Find these four users & which sites they (each) visited more than 10 times. 
        (Simply provides four triples in the form (user_id, site_id, number of visits) in the box below.)
    """
    print('Find these four users & which sites they (each) visited more than 10 times:')
    print(find_site_visitors(min_visit_num_per_site=10,
                             start_datetime='2019-02-03 00:00:00',
                             end_datetime='2019-02-04 23:59:59'))
    print('')

    """
        CASE 3
        For each site, compute the unique number of users whose last visit 
        (found in the original data set) was to that site. 
        For instance, user "LC3561"'s last visit is to "N0OTG" based on timestamp data. 
        Based on this measure, what are top three sites? 
        (hint: site "3POLC" is ranked at 5th with 28 users whose last visit in the data set was to 3POLC; 
        simply provide three pairs in the form (site_id, number of users).)
    """
    print('what are top three sites where the unique number of users whose last visit?:')
    print(find_top_sites_visited_last_time())
    print('')

    """
        CASE 4
        For each user, determine the first site he/she visited 
        and the last site he/she visited based on the timestamp data. 
        Compute the number of users whose first/last visits are to the same website. 
        What is the number?
    """
    print('Compute the number of users whose first/last visits are to the same website. \n'
          'What is the number?:')
    print(find_users_with_same_first_last_visit_sites())
    print('')
