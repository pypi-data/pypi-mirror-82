"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional, Union

import toml

from statue.command import Command
from statue.constants import (
    ADD_ARGS,
    ARGS,
    CLEAR_ARGS,
    COMMANDS,
    CONTEXTS,
    DEFAULT_CONFIGURATION_FILE,
    HELP,
    OVERRIDE,
    PARENT,
    SOURCES,
    STANDARD,
    STATUE,
)
from statue.exceptions import (
    EmptyConfiguration,
    InvalidCommand,
    InvalidStatueConfiguration,
    MissingConfiguration,
    UnknownCommand,
    UnknownContext,
)


class Configuration:
    """Configuration singleton for statue."""

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None

    @classmethod
    def configuration_path(cls, directory: Union[Path, str]) -> Path:
        """Get default path of configuration file in directory."""
        if isinstance(directory, str):
            directory = Path(directory)
        return directory / "statue.toml"

    @classmethod
    def default_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of default configuration."""
        if cls.__default_configuration is None:
            cls.__load_default_configuration()
        return deepcopy(cls.__default_configuration)

    @classmethod
    def set_default_configuration(
        cls, default_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of default configuration."""
        cls.__default_configuration = default_configuration

    @classmethod
    def statue_configuration(cls) -> MutableMapping[str, Any]:
        """Getter of general statue configuration."""
        if cls.__statue_configuration is not None:
            return deepcopy(cls.__statue_configuration)
        default_configuration = cls.default_configuration()
        if default_configuration is not None:
            return default_configuration
        raise EmptyConfiguration()

    @classmethod
    def set_statue_configuration(
        cls, statue_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of general statue configuration."""
        cls.__statue_configuration = statue_configuration

    @classmethod
    def commands_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of the commands configuration."""
        return cls.statue_configuration().get(COMMANDS, None)

    @classmethod
    def commands_names_list(cls) -> List[str]:
        """Getter of the commands list."""
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            return []
        return list(commands_configuration.keys())

    @classmethod
    def get_command_configuration(
        cls, command_name: str
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Get configuration dictionary of a context.

        :param command_name: Name of the desired command.
        :type command_name: str
        :return: configuration dictionary.
        :raises: raise :Class:`MissingConfiguration` if no contexts configuration was
        set.
        """
        commands_configuration = cls.commands_configuration()
        if commands_configuration is None:
            raise MissingConfiguration(COMMANDS)
        return commands_configuration.get(command_name, None)

    @classmethod
    def sources_configuration(
        cls,
    ) -> MutableMapping[str, MutableMapping[str, Any]]:
        """Getter of the sources configuration."""
        sources_configuration: Optional[
            MutableMapping[str, MutableMapping[str, Any]]
        ] = cls.statue_configuration().get(SOURCES, None)
        if sources_configuration is None:
            raise MissingConfiguration(SOURCES)
        return sources_configuration

    @classmethod
    def sources_list(cls) -> List[str]:
        """Getter of the commands list."""
        return list(cls.sources_configuration().keys())

    @classmethod
    def get_source_configuration(
        cls, source: Union[Path, str]
    ) -> MutableMapping[str, Any]:
        """
        Get configuration dictionary of a context.

        :param source: Name of the desired source.
        :type source: str
        :return: configuration dictionary.
        :raises: raise :Class:`MissingConfiguration` if no contexts configuration was
        set.
        """
        source_configuration = cls.sources_configuration()
        if isinstance(source, Path):
            source = str(source)
        return source_configuration.get(source, {})

    @classmethod
    def contexts_configuration(cls) -> Optional[MutableMapping[str, Any]]:
        """Getter of the contexts configuration."""
        return cls.statue_configuration().get(CONTEXTS, None)

    @classmethod
    def get_context_configuration(
        cls, context_name: str
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Get configuration dictionary of a context.

        :param context_name: Name of the desired context.
        :type context_name: str
        :return: configuration dictionary.
        :raises: raise :Class:`MissingConfiguration` if no contexts configuration was
        set.
        """
        contexts_configuration = cls.contexts_configuration()
        if contexts_configuration is None:
            raise MissingConfiguration(CONTEXTS)
        return contexts_configuration.get(context_name, None)

    @classmethod
    def read_commands(
        cls,
        contexts: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ) -> List[Command]:
        """
        Read commands from a settings file.

        :param contexts: List of str. a list of contexts to choose commands from.
        :param allow_list: List of allowed commands. If None, take all commands
        :param deny_list: List of denied commands. If None, take all commands
        :return: a list of :class:`Command`
        """
        commands = []
        contexts = [] if contexts is None else contexts
        for command_name in cls.commands_names_list():
            try:
                commands.append(
                    cls.read_command(
                        command_name=command_name,
                        contexts=contexts,
                        allow_list=allow_list,
                        deny_list=deny_list,
                    )
                )
            except InvalidCommand:
                continue
        return commands

    @classmethod
    def read_command(
        cls,
        command_name: str,
        contexts: Optional[List[str]] = None,
        allow_list: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ) -> Command:
        """
        Read command from a settings file.

        :param command_name: the name of the command to read.
        :param contexts: List of str. a list of contexts to choose commands from.
        :param allow_list: List of allowed commands. If None, take all commands
        :param deny_list: List of denied commands. If None, take all commands
        :return: a :class:`Command` instance
        :raises: :class:`UnknownCommand` if command is missing from settings file.
        :class:`InvalidCommand` of command doesn't fit the given contexts, allow list
         and deny list
        """
        command_configuration = cls.get_command_configuration(command_name)
        if command_configuration is None:
            raise UnknownCommand(command_name)
        if not cls.__is_command_matching(
            command_name, command_configuration, contexts, allow_list, deny_list
        ):
            raise InvalidCommand(
                command_name=command_name,
                contexts=contexts,
                allow_list=allow_list,
                deny_list=deny_list,
            )
        contexts = [] if contexts is None else contexts
        for context in contexts:
            context_obj = command_configuration.get(context, None)
            if not isinstance(context_obj, dict):
                continue
            command_configuration = cls.__combine_command_setups(
                command_configuration, context_obj
            )
        return Command(
            name=command_name,
            args=command_configuration.get(ARGS, []),
            help=command_configuration[HELP],
        )

    @classmethod
    def load_configuration(
        cls,
        statue_configuration_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
        repository-specific configurations
        """
        if statue_configuration_path is None:
            statue_configuration_path = cls.configuration_path(Path.cwd())
        if isinstance(statue_configuration_path, str):
            statue_configuration_path = Path(statue_configuration_path)
        cls.set_statue_configuration(
            cls.__build_configuration(statue_configuration_path)
        )

    @classmethod
    def reset_configuration(cls) -> None:
        """Reset the general statue configuration."""
        cls.set_default_configuration(None)
        cls.set_statue_configuration(None)

    @classmethod
    def __load_default_configuration(cls) -> None:
        if not DEFAULT_CONFIGURATION_FILE.exists():
            return
        cls.set_default_configuration(toml.load(DEFAULT_CONFIGURATION_FILE))

    @classmethod
    def __build_configuration(
        cls,
        statue_configuration_path: Path,
    ) -> Optional[MutableMapping[str, Any]]:
        """
        Build statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
        repository-specific configurations
        """
        if not statue_configuration_path.exists():
            return None
        statue_config = toml.load(statue_configuration_path)
        default_configuration = cls.default_configuration()
        if default_configuration is None:
            return statue_config
        general_settings = statue_config.get(STATUE, None)
        if general_settings is not None and general_settings.get(OVERRIDE, False):
            return statue_config
        commands_configuration = cls.__build_commands_configuration(
            statue_commands_configuration=statue_config.get(COMMANDS, None),
            default_commands_configuration=default_configuration.get(COMMANDS, None),
        )
        if commands_configuration is not None:
            statue_config[COMMANDS] = commands_configuration
        contexts_configuration = cls.__build_contexts_configuration(
            statue_contexts_configuration=statue_config.get(CONTEXTS, None),
            default_contexts_configuration=default_configuration.get(CONTEXTS, None),
        )
        if contexts_configuration is not None:
            statue_config[CONTEXTS] = contexts_configuration
        return statue_config

    @classmethod
    def __build_commands_configuration(
        cls,
        statue_commands_configuration: Optional[MutableMapping[str, Any]],
        default_commands_configuration: Optional[MutableMapping[str, Any]],
    ) -> Optional[MutableMapping[str, Any]]:
        if statue_commands_configuration is None:
            return default_commands_configuration
        if default_commands_configuration is None:
            return statue_commands_configuration
        commands_configuration = deepcopy(default_commands_configuration)
        for command_name, command_setups in statue_commands_configuration.items():
            if command_name in commands_configuration:
                commands_configuration[command_name] = cls.__combine_command_setups(
                    commands_configuration[command_name], command_setups
                )
            else:
                commands_configuration[command_name] = command_setups
        return commands_configuration

    @classmethod
    def __build_contexts_configuration(
        cls,
        statue_contexts_configuration: Optional[MutableMapping[str, Any]],
        default_contexts_configuration: Optional[MutableMapping[str, Any]],
    ) -> Optional[MutableMapping[str, Any]]:
        if statue_contexts_configuration is None:
            return default_contexts_configuration
        if default_contexts_configuration is None:
            return statue_contexts_configuration
        contexts = deepcopy(default_contexts_configuration)
        for context_name, context_setup in statue_contexts_configuration.items():
            if context_name in contexts:
                raise InvalidStatueConfiguration(
                    f'"{context_name}" is a predefined context and cannot be override'
                )
            contexts[context_name] = context_setup
        return contexts

    @classmethod
    def __is_command_matching(  # pylint: disable=too-many-arguments
        cls,
        command_name: str,
        setups: MutableMapping[str, Any],
        contexts: Optional[List[str]],
        allow_list: Optional[List[str]],
        deny_list: Optional[List[str]],
    ) -> bool:
        """
        Check whether a command fits the restrictions or not.

        :param command_name: the name of the command to read.
        :param setups: Dictionary. The command's configuration.
        :param contexts: List of str. a list of contexts.
        :param allow_list: List of allowed commands.
        :param deny_list: List of denied commands.
        :return: Boolean. Does the command fit the restrictions
        """
        if deny_list is not None and command_name in deny_list:
            return False
        if (
            allow_list is not None
            and len(allow_list) != 0  # noqa: W503
            and command_name not in allow_list  # noqa: W503
        ):
            return False
        if contexts is None or len(contexts) == 0:
            return cls.__command_match_default_context(setups)
        for command_context in contexts:
            if not cls.__command_match_context(setups, command_context):
                return False
        return True

    @classmethod
    def __command_match_context(
        cls, setups: MutableMapping[str, Any], context_name: str
    ) -> bool:
        if context_name == STANDARD:
            return cls.__command_match_default_context(setups)
        context_configuration = cls.get_context_configuration(context_name)
        if context_configuration is None:
            raise UnknownContext(context_name)
        if setups.get(context_name, False):
            return True
        parent_context = context_configuration.get(PARENT, None)
        if parent_context is not None:
            return cls.__command_match_context(setups, parent_context)
        return False

    @classmethod
    def __command_match_default_context(cls, setups: MutableMapping[str, Any]) -> bool:
        return setups.get(STANDARD, True)

    @classmethod
    def __combine_command_setups(
        cls,
        base_setup: MutableMapping[str, Any],
        setup: MutableMapping[str, Any],
    ) -> MutableMapping[str, Any]:
        new_setup = cls.__remove_args_keys(base_setup)
        args = cls.__combine_command_args(base_setup.get(ARGS, None), setup)
        if args is not None:
            new_setup[ARGS] = args
        new_setup.update(cls.__remove_args_keys(setup))
        return new_setup

    @classmethod
    def __combine_command_args(
        cls, base_args: Optional[List[str]], command_setup: MutableMapping[str, Any]
    ) -> Optional[List[str]]:
        base_args = [] if base_args is None else base_args
        args: List[str] = command_setup.get(ARGS, None)
        if args is not None:
            return args
        add_args = command_setup.get(ADD_ARGS, None)
        if add_args is not None:
            return base_args + add_args
        clear_args = command_setup.get(CLEAR_ARGS, False)
        if clear_args:
            return None
        if len(base_args) == 0:
            return None
        return base_args

    @classmethod
    def __remove_args_keys(
        cls, command_setup: MutableMapping[str, Any]
    ) -> MutableMapping[str, Any]:
        return {
            key: value
            for key, value in command_setup.items()
            if key not in [ARGS, ADD_ARGS, CLEAR_ARGS]
        }
