import pygsheets
# import pandas as pd

gc = pygsheets.authorize(
    service_file='verified-security-sources-6b7e7530d6f5.json')
sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1ELBSsc5tQIjZFHCmTofbwflOx37CK0OOpXEiMa2Irto/edit?usp=sharing")

# wk1 = sh[0]
first_column_data = sh[0].get_col(1, include_tailing_empty=False)[1:]
usernames_list = [row.replace('https://twitter.com/', 'from:')
                  for row in first_column_data]
# print(usernames_list)

username_rule = " OR ".join(usernames_list)
# for username in usernames_list:
# username_rule = username_rule + "from:" + username + " OR "
print(username_rule)
