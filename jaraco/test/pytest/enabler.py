import contextlib
import shlex
import types
import sys

import toml
from jaraco.context import suppress
from jaraco.functools import apply


def none_as_empty(ob):
    """
    >>> none_as_empty({})
    {}
    >>> none_as_empty(None)
    {}
    >>> none_as_empty({'a': 1})
    {'a': 1}
    """
    return ob or {}


@apply(none_as_empty)
@suppress(Exception)
def read_plugins(filename):
    with open(filename) as strm:
        defn = toml.load(strm)
    return defn["tool"]["jaraco"]["pytest"]["plugins"]


def pytest_load_initial_conftests(early_config, parser, args):
    plugins = read_plugins('pyproject.toml')
    matches = filter(early_config.pluginmanager.has_plugin, plugins)
    for match in matches:
        args.extend(shlex.split(plugins[match].get('addopts', "")))
    _pytest_cov_check(plugins, early_config, parser, args)


def _remove_deps():
    """
    Coverage will not detect function definitions as being covered
    if the functions are defined before coverage is invoked. As
    a result, when testing any of the dependencies above, their
    functions will appear not to be covered. To avoid this behavior,
    unload the modules above so they may be tested for coverage
    on import as well.
    """
    del sys.modules['jaraco.functools']
    del sys.modules['jaraco.context']
    del sys.modules['toml']


def _pytest_cov_check(plugins, early_config, parser, args):  # pragma: nocover
    """
    pytest_cov runs its command-line checks so early that no hooks
    can intervene. By now, the hook that installs the plugin has
    already run and failed to enable the plugin. So, parse the config
    specially and re-run the hook.
    """
    new_args = shlex.split(plugins.get('cov', {}).get('addopts', ""))
    plugin_enabled = any(
        plugin.__name__.startswith('pytest_cov.')
        for plugin in early_config.pluginmanager.get_plugins()
        if isinstance(plugin, types.ModuleType)
    )
    if not new_args or not plugin_enabled:
        return
    _remove_deps()
    parser.parse_known_and_unknown_args(new_args, early_config.known_args_namespace)
    with contextlib.suppress(ImportError):
        import pytest_cov.plugin

        pytest_cov.plugin.pytest_load_initial_conftests(early_config, parser, args)
