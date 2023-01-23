#!/usr/bin/env python

# requires: gitpython

import os
from argparse import ArgumentParser

from git import Repo


KEYWORDS = ['nopackage', 'deploy', 'docs']
EXISTING_PACKAGES = []


def prefix_invalid(prefix):
    if prefix.strip() not in EXISTING_PACKAGES and prefix not in KEYWORDS:
        return True

    return False


def main(title):
    repo = Repo('.')

    faulty_commits = []

    prefix = title.split(':')[0]
    if prefix_invalid(prefix):
        msg = '* Merge Request Title\n'
        msg += f'> {title}\n\n'
        msg += 'Merge request title needs to be compliant as well, '
        msg += 'as it will be used for the merge/squash commit'
        faulty_commits.append(msg)

    for commit in repo.iter_commits():
        print(f'Commit: {commit.message} (parents: {commit.parents})')
        if len(commit.parents) > 1:
            print('Not going beyond a merge commit')
            break

        prefix = commit.message.splitlines()[0].split(':')[0]
        if prefix_invalid(prefix):
            quoted_commit_message = '\n'.join([f'> {line}' for
                                               line in commit.message.splitlines()])
            msg = f'* {commit.hexsha}\n'
            msg += f'{quoted_commit_message}'
            faulty_commits.append(msg)

    if faulty_commits:
        warning = 'These commits are not formatted correctly. '
        warning += 'Please amend them to start with one of:\n'
        warning += '* \\<package>: \n'
        warning += f'* {", ".join(keyword + ":" for keyword in KEYWORDS)}\n\n'
        warning += "### Faulty commits:\n"
        faulty_commits.insert(0, warning)
        with open('faulty_commits.txt', 'w') as fp:
            fp.write('\n'.join(faulty_commits))
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fp:
            fp.write("faulty-commits=true")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--title", required=True, help="PR title")

    args = parser.parse_args()

    for spack_repo in ['./var/spack/repos/builder.test',
                       './var/spack/repos/builtin',
                       './var/spack/repos/builtin.mock',
                       './var/spack/repos/tutorial',
                       './bluebrain/repo-bluebrain',
                       './bluebrain/repo-patches']:
        try:
            EXISTING_PACKAGES.extend(next(os.walk(f'{spack_repo}/packages'))[1])
        except StopIteration:
            print(f'No packages under {spack_repo}')
            pass

    main(args.title)
