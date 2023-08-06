import sys
import os
import os.path as p
import click
from ..shared_vars import (pandoctools_user, pandoctools_user_data, pandoctools_core,
                           PandotoolsError, bash_cygpath)


def main(basename: str, fallback_basename: str=None) -> str:
    """
    Returns Unix style absolute path to the file by its basename (given with extension).
    First searches in $HOME/.pandoc/pandoctools (or %APPDATA%\\pandoc\\pandoctools),
    Then in Pandoctools module directory  (<...>/site-packages/pandoctools/sh).
    Fallback basename is used if the first one wasn't found.
    
    On Windows conversion to POSIX paths is done via cygpath that at first is read from
    $cygpath env var then seached in the current python environment, near bash executable,
    in the $PATH

    :param basename:
    :param fallback_basename:
    :return: absolute path (or empty string if it wasn't found)
    """
    for abs_path in (p.join(dir_, name)
                     for name in (basename, fallback_basename)
                     for dir_ in (pandoctools_user, pandoctools_core)
                     if name):
        if p.isfile(abs_path):
            if os.name == 'nt':
                from subprocess import run, PIPE
                cygpath = os.environ.get('cygpath')
                cygpath = bash_cygpath()[1] if not cygpath else cygpath
                return run([cygpath, abs_path], stdout=PIPE, encoding='utf-8').stdout
            else:
                return abs_path
    raise PandotoolsError(f"'{basename}' or fallback '{fallback_basename}'" +
                          f" wasn't found in '{pandoctools_user}' and '{pandoctools_core}'.")


@click.command(help=f"""
Inside Pandoctools shell scripts use alias: $resolve

Resolves and echoes Unix style absolute path to the file by its basename (given with extension).
First searches in {pandoctools_user_data}, then in Pandoctools module directory:
{pandoctools_core}

On Windows conversion to POSIX paths is done via cygpath that at first is read from
$cygpath env var then seached in the current python environment, near bash executable,
in the $PATH
""")
@click.argument('file_basename', type=str)
@click.option('--else', 'fallback', type=str, default=None,
              help="Fallback file basename that is used if the first one wasn't found.")
def cli(file_basename, fallback):
    sys.stdout.write(main(file_basename, fallback))
