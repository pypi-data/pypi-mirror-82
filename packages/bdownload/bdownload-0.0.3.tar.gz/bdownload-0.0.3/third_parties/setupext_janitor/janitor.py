from distutils import dir_util, errors, log
from distutils.command.clean import clean as _CleanCommand
import os.path

# import setupext_janitor

# backwards compat -- WILL BE REMOVED IN THE FUTURE
# version_info = setupext_janitor.version_info
# __version__ = setupext_janitor.version

# debug = False


class CleanCommand(_CleanCommand):
    """
    Extend the clean command to do additional house keeping.

    The traditional distutils clean command removes the by-products of
    compiling extension code.  This class extends it to remove the
    similar by-products generated by producing a Python distribution.
    Most notably, it will remove .egg/.egg-info directories, the
    generated distribution, those pesky *__pycache__* directories,
    and even the virtual environment that it is running in.

    The level of cleanliness is controlled by command-line options as
    you might expect.  The targets that are removed are influenced by
    the commands that created them.  For example, if you set a custom
    distribution directory using the ``--dist-dir`` option or the
    matching snippet in *setup.cfg*, then this extension will honor
    that setting.  It even goes as far as to detect the virtual
    environment directory based on environment variables.

    This all sounds a little dangerous... there is little to worry
    about though.  This command only removes what it is configured to
    remove which is nothing by default.  It also honors the
    ``--dry-run`` global option so that there should be no question
    what it is going to remove.

    """

    # See _set_options for `user_options`

    def initialize_options(self):
        _CleanCommand.initialize_options(self)
        self.build = False
        self.dist = False
        self.eggs = False
        self.egg_base = None
        self.environment = False
        self.pycache = False
        self.virtualenv_dir = None

    def finalize_options(self):
        _CleanCommand.finalize_options(self)
        try:
            self.set_undefined_options(
                'egg_info', ('egg_base', 'egg_base'))
        except errors.DistutilsError:
            pass

        if self.egg_base is None:
            self.egg_base = os.curdir

        if self.all:
            for flag in self.boolean_options:
                if flag != 'environment':  # FIXME
                    setattr(self, flag, True)

        if self.environment and self.virtualenv_dir is None:
            self.virtualenv_dir = os.environ.get('VIRTUAL_ENV', None)

    def run(self):
        _CleanCommand.run(self)

        dir_names = set()
        if self.build:
            dir_names.update(_gather_attributes(
                self.distribution,
                lambda cmd_name: cmd_name.startswith('build'),
                'build_base', 'build_clib', 'build_dir', 'build_lib',
                'build_temp'))

        if self.dist:
            dir_names.update(_gather_attributes(
                self.distribution, lambda cmd_name: 'dist' in cmd_name,
                'dist_dir'))

        if self.eggs:
            for name in os.listdir(self.egg_base):
                if name.endswith('.egg-info'):
                    dir_names.add(os.path.join(self.egg_base, name))
            for name in os.listdir(os.curdir):
                for e in ['.egg', '.eggs', '.egg-info']:  # FIXME
                    if name.endswith(e):
                        dir_names.add(name)

        if self.environment and self.virtualenv_dir:
            dir_names.add(self.virtualenv_dir)

        if self.pycache:
            for root, dirs, _ in os.walk(os.curdir):
                if '__pycache__' in dirs:
                    dir_names.add(os.path.join(root, '__pycache__'))

        for dir_name in dir_names:
            if os.path.exists(dir_name):
                dir_util.remove_tree(dir_name, dry_run=self.dry_run)
            else:
                self.announce(
                    'skipping {0} since it does not exist'.format(dir_name))


def _gather_attributes(dist, selector, *attributes):
    """Gather arbitrary attributes from a select set of commands.

    :param distutils.dist.Distribution dist: distribution to process
    :param selector: callable that selects which commands to process
        by name.  selector(str) -> bool.
    :param attributes: list of attribute names to gather
    :rtype: set[str]

    This function iterates over the commands available in `dist`,
    ensures that the are finalized, and returns the values of the
    attributes listed in `attributes`.  It only processes commands
    that are selected by `selector` which is a callable that takes
    a command name and returns :data:`True` or :data:`False`.

    """
    dir_names = set()
    for cmd_name, _ in dist.get_command_list():
        if selector(cmd_name):
            command = dist.get_command_obj(cmd_name)
            try:
                command.ensure_finalized()
                for name in attributes:
                    dir_name = getattr(command, name, None)
                    if dir_name:
                        dir_names.add(dir_name)
            except errors.DistutilsPlatformError as err:
                # This isn't science, but it seems to work.  I decided to
                # ignore platform errors during command finalization since
                # they indicate that the particular command is not supported
                # on the current platform.  See
                # https://github.com/dave-shawley/setupext-janitor/issues/12
                # for the initial defect discussion.
                log.warn('ignoring error from %s: %s', cmd_name, err)
    return dir_names


def _set_options():
    """
    Set the options for CleanCommand.

    There are a number of reasons that this has to be done in an
    external function instead of inline in the class.  First of all,
    the setuptools machinery really wants the options to be defined
    in a class attribute - otherwise, the help command doesn't work
    so we need a class attribute.  However, we are extending an
    existing command and do not want to "monkey patch" over it so
    we need to define a *new* class attribute with the same name
    that contains a copy of the base class value.  This could be
    accomplished using some magic in ``__new__`` but I would much
    rather set the class attribute externally... it's just cleaner.

    """
    CleanCommand.user_options = _CleanCommand.user_options[:]
    CleanCommand.user_options.extend([
        ('build', 'b', 'remove build directory'),
        ('dist', 'd', 'remove distribution directory'),
        ('eggs', None, 'remove egg and egg-info directories'),
        ('environment', 'E', 'remove virtual environment directory'),
        ('pycache', 'p', 'remove __pycache__ directories'),

        ('egg-base=', 'e',
         'directory containing .egg-info directories '
         '(default: top of the source tree)'),
        ('virtualenv-dir=', None,
         'root directory for the virtual directory '
         '(default: value of VIRTUAL_ENV environment variable)'),
    ])
    CleanCommand.boolean_options = _CleanCommand.boolean_options[:]
    CleanCommand.boolean_options.extend(
        ['dist', 'eggs', 'environment', 'pycache'])


_set_options()
