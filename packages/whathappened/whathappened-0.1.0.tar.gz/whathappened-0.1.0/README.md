[![GitHub license](https://img.shields.io/github/license/Rollcloud/whathappened)](https://github.com/Rollcloud/whathappened/blob/main/LICENSE)
![semver](https://img.shields.io/badge/semver-2.0.0-blue)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/rollcloud/whathappened?sort=semver)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/Rollcloud/whathappened/latest/develop?sort=semver)

# whathappened
A changelog generator using simply structured git commit messages

## Inspired by

* [SemVer](https://semver.org/)
* [Angular Commit Message Format](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
* [Auto Changelog](https://github.com/Michael-F-Bryan/auto-changelog)
* [git_commits.py](https://gist.github.com/simonw/091b765a071d1558464371042db3b959#file-get_commits-py)


## Whathappened Commit Message Format

Whathappened expects git commit messages in the format outlined below:

    [optional breaking ]<type>[ optional (<scope>)]: <description>

    [optional body]

`<type>` is recommended to be one of:

    fix
    feat
    build
    chore
    ci
    docs
    style
    refactor
    perf
    test

`<scope>` is recommended to be a module, file, or folder name as appropiate.

This is a simpler version of https://www.conventionalcommits.org/
