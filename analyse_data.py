import pickle
from functools import cmp_to_key
import sys

if len(sys.argv) != 2:
    print("you gotta put a filename and ONLY a filename")
    exit()

fn = sys.argv[1]

data = pickle.load(open(fn, "rb"))

all_tags = dict()
all_accounts = dict()


def add_account(account, likes):
    if account in all_accounts:
        all_accounts[account] += 1
    else:
        all_accounts[account] = 1


def add_tag(tag, likes):
    if tag in all_tags:
        all_tags[tag]["likes"] += likes
        all_tags[tag]["count"] += 1
    else:
        all_tags[tag] = dict(tagname=tag, likes=likes, count=1)


for i in data:
    account_name = i[0]
    likes = int(i[1])
    tags = i[2]
    for tag in tags:
        add_tag(tag, likes)
    add_account(account_name, likes)
    # print(account_name, likes)

for a in all_accounts:
    if all_accounts[a] > 1:
        print("{} {}".format(a, all_accounts[a]))

tag_list = []
for t in all_tags:
    tag_list.append(all_tags[t])
    if all_tags[t]["count"] > 10:
        print("{} {}".format(t, all_tags[t]["count"]))


def compare(i1, i2):
    if i1["count"] < i2["count"]:
        return 1
    elif i1["count"] > i2["count"]:
        return -1
    else:
        return 0


def print_tag_list(list_to_print):
    print("----------")
    for x in range(25):
        t = list_to_print[x]
        print(
            "{} {} {}".format(
                str.ljust(t["tagname"], 25),
                str.rjust(str(t["count"]), 5),
                str.rjust(str(t["likes"]), 5),
            )
        )


print_tag_list(sorted(tag_list, key=cmp_to_key(compare)))
