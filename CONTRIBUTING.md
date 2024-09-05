<!-- omit in toc -->
# Contributing to APIS

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of
Contents](#table-of-contents) for different ways to help and details about how
this project handles them. Please make sure to read the relevant section before
making your contribution. It will make it a lot easier for us maintainers and
smooth out the experience for all involved. The community looks forward to your
contributions. 🎉

<!-- omit in toc -->
## Table of Contents

- [I Have a Question](#i-have-a-question)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)



## I Have a Question

If you want to ask a question, we assume that you have read the available
[Documentation](https://acdh-oeaw.github.io/apis-core-rdf/).

Before you ask a question, it is best to search for existing
[Issues](https://github.com/acdh-oeaw/apis-core-rdf/issues) that might help
you. In case you have found a suitable issue and still need clarification, you
can write your question in this issue. It is also advisable to search the
internet for answers first.

If you then still feel the need to ask a question and need clarification, we
recommend the following:

- Open an [Issue](https://github.com/acdh-oeaw/apis-core-rdf/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions, depending on what seems relevant.

We will then take care of the issue as soon as possible.

## Styleguides

Please try to keep your commit changes focused on the change you want to
implement - don't start fixing typos if your commit is actually about adding a
feature.

We use [ruff](https://docs.astral.sh/ruff/) for linting and
code formatting and [djlint](https://djlint.com/) for
formatting templates - the configuration for those is part of our
[`pyproject.toml`](https://github.com/acdh-oeaw/apis-core-rdf/blob/main/pyproject.toml).
We also check the code using the [deptry](https://deptry.com/)
dependency checker for missing or unused dependencies.

Base your commit on the latest changes in `main`. Your work might take some
time and other people are also working on APIS, so please rebase your changes
early and often.

### Commit Messages

We use [conventional
commits](https://www.conventionalcommits.org/en/v1.0.0/) so please format your
commit messages accordingly. There is a GitHub Action that uses the
[Gitlint](https://jorisroovers.com/gitlint/latest/) linter to check your commit
messages for validity.

Please try to use a scope when writing a commit message. APIS consists of
various individual modules, so the scope tells the users which module your
change refers to.

Examples:
> `feat(apis_entities): introduce a e53_place autocomplete template`

([ac358a7e](https://github.com/acdh-oeaw/apis-core-rdf/commit/ac358a7e7d915e756f2de776d5ba95854bb5bd5e))

or

> `fix(apis_relations,apis_entities): replace get_object_or_404`

([6785b802](https://github.com/acdh-oeaw/apis-core-rdf/commit/6785b802f3de88d2cd6d7202bbd88cf9320e1bed))

Feel free to browse our commit history to get an idea how commit messages
should look like.

We use the [release-please](https://github.com/googleapis/release-please)
GitHub Action, which uses the information from the conventional commit messages
to generate changelogs and bump the version. Therefore it is important to use
the correct commit type in the commit message, i.e. `fix` for smaller fixes,
`feat` for new features. Breaking changes have to have an exclamation mark
(`!`) after the type/scope, but please also explain the breaking change in the
commit message body.

An example how a resulting changelog could look like would be [the changelog of
release 0.26.0](https://github.com/acdh-oeaw/apis-core-rdf/releases/tag/v0.26.0).
Feel free to browse the [releases](https://github.com/acdh-oeaw/apis-core-rdf/releases)
and the [CHANGELOG](CHANGELOG.md) file.


## Workflows

You can see a list of worklows which are run on pull requests
[here](https://github.com/acdh-oeaw/apis-core-rdf/tree/main/.github/workflows).

<!-- omit in toc -->
## Attribution
This guide is loosely based on the **contributing-gen**. [Make your
own](https://github.com/bttger/contributing-gen)!
