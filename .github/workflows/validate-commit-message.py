#!/usr/bin/env python

# requires: gitpython

import os
from argparse import ArgumentParser

from git import Repo


def main(title):
    keywords = ['nopackage', 'deploy']

    repo = Repo('.')

    existing_packages = []
    for spack_repo in ['./var/spack/repos/builder.test',
                       './var/spack/repos/builtin',
                       './var/spack/repos/builtin.mock',
                       './var/spack/repos/tutorial',
                       './bluebrain/repo-bluebrain',
                       './bluebrain/repo-patches']:
        try:
            existing_packages.extend(next(os.walk(f'{spack_repo}/packages'))[1])
        except StopIteration:
            print(f'No packages under {spack_repo}')
            pass

    faulty_commits = []

    package = title.split(':')[0]
    if package.strip() not in existing_packages and package not in keywords:
        msg = f'* Merge Request Title\n'
        msg += f'> {title}\n\n'
        msg += 'Merge request title needs to be compliant as well, '
        msg += 'as it will be used for the merge/squash commit'
        faulty_commits.append(msg)

    for commit in repo.iter_commits():
        print(f'Commit: {commit.message} (parents: {commit.parents})')
        if len(commit.parents) > 1:
            print('Not going beyond a merge commit')
            break

        package = commit.message.splitlines()[0].split(':')[0]
        if package.strip() not in existing_packages and package not in keywords:
            quoted_commit_message = '\n'.join([f'> {line}' for line in commit.message.splitlines()])
            msg = f'* {commit.hexsha}\n'
            msg += f'{quoted_commit_message}'
            faulty_commits.append(msg)

    if faulty_commits:
        warning = 'These commits are not formatted correctly. Please amend them to start with one of:\n'
        warning += '* \\<package>: \n'
        warning += f'* {", ".join(keyword + ":" for keyword in keywords)}\n\n'
        warning += "### Faulty commits:\n"
        faulty_commits.insert(0, warning)
        with open('faulty_commits.txt', 'w') as fp:
            fp.write('\n'.join(faulty_commits))
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fp:
            fp.write("faulty-commits=true")
    #else:
    #    with open('faulty_commits.txt', 'w') as fp:
    #        fp.write("All commit messages are good")
    #    with open(os.environ['GITHUB_OUTPUT'], 'a') as fp:
    #        fp.write("faulty-commits=false")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--title", required=True, help="PR title")

    args = parser.parse_args()
    main(args.title)
