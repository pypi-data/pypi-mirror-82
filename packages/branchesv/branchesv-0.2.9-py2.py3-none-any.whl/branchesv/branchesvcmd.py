# -*- coding: utf-8 -*-

import click
from . import branches, utils


@click.group()
def cli():
    pass


@cli.command()
@click.option("-f", "--json-file", help="Json file to use", required=True)
@click.option("-p", "--path", required=True,
              help="Path of GIT Repo, actual dir by default. May be a list for save option",
              default=None)
@click.option("--recursive/--no-recursive", default=True,
              help="Sets the search of repositories as recursive or no recursive. Recursive by default")
def save(json_file, path, recursive):
    """save command
    """
    branches.save(json_file, path, recursive)


@cli.command()
@click.option("-f", "--json-file", help="Json file to use", required=True)
@click.option("-p", "--path", required=True,
              help="Path of GIT Repo, actual dir by default. May be a list for save option",
              default=None)
@click.option("--tmp", help="Temporary directory for branches files",
              default="/tmp")
@click.option("-k", "--key-ssh", help="The SSH private key that will use to clone/pull the repositories",
              default=False)
def load(json_file, path, tmp, key_ssh):
    repos = utils.load_json(json_file)
    branches.load(repos, path, tmp, key_ssh)


@cli.command()
@click.option("-p", "--path",
              help="Path of GIT Repo, actual dir by default. May be a list",
              default=None, required=True)
@click.option("--tmp", help="Temporary directory for branches files",
              default="/tmp")
@click.option("--recursive/--no-recursive", default=True,
              help="Sets the search of repositories as recursive or no recursive. Recursive by default")
@click.option("-k", "--key-ssh", help="The SSH private key that will use to pull the repository",
              default=False)
def pull(path, tmp, recursive, key_ssh):
    branches.pull(path, tmp, recursive, key_ssh)
