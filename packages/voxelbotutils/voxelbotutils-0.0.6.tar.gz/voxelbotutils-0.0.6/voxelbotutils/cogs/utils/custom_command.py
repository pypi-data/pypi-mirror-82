import datetime
import typing

from discord.ext import commands

from .checks.meta_command import InvokedMetaCommand


class CustomCommand(commands.Command):
    """
    A custom command object for wrapping our commands with.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, cooldown_after_parsing=kwargs.pop('cooldown_after_parsing', True), **kwargs)
        self.ignore_checks_in_help: bool = kwargs.get('ignore_checks_in_help', False)

        # Fix cooldown to be our custom type
        cooldown = self._buckets._cooldown
        if cooldown is None:
            mapping = commands.CooldownMapping  # No mapping
        elif getattr(cooldown, 'mapping', None) is not None:
            mapping = cooldown.mapping  # There's a mapping in the instance
        elif getattr(cooldown, 'default_mapping_class') is not None:
            mapping = cooldown.default_mapping_class()  # Get the default mapping from the object
        else:
            raise ValueError("No mapping found for cooldown")
        self._buckets = mapping(cooldown)  # Wrap the cooldown in the mapping

    def get_remaining_cooldown(self, ctx:commands.Context, current:float=None) -> typing.Optional[float]:
        """
        Gets the remaining cooldown for a given command.

        Args:
            ctx (commands.Context): The context object for the command/author.
            current (float, optional): The current time.

        Returns:
            typing.Optional[float]: The remaining time on the user's cooldown or `None`.
        """

        bucket = self._buckets.get_bucket(ctx.message)
        return bucket.get_remaining_cooldown()

    def _prepare_cooldowns(self, ctx:commands.Context):
        """
        Prepares all the cooldowns for the command to be called.
        """

        if self._buckets.valid:
            current = ctx.message.created_at.replace(tzinfo=datetime.timezone.utc).timestamp()
            bucket = self._buckets.get_bucket(ctx.message, current)
            try:
                bucket.predicate(ctx)
            except AttributeError:
                ctx.bot.logger.critical(f"Invalid cooldown set on command {ctx.invoked_with}")
                raise commands.CheckFailure("Invalid cooldown set for this command")
            retry_after = bucket.update_rate_limit(current)
            if retry_after:
                try:
                    error = bucket.error
                except AttributeError:
                    error = bucket.default_cooldown_error
                raise error(bucket, retry_after)


class CustomGroup(commands.Group):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, cooldown_after_parsing=kwargs.get('cooldown_after_parsing', True), **kwargs)
        self.ignore_checks_in_help = kwargs.get('ignore_checks_in_help', False)

    async def can_run(self, ctx:commands.Context) -> bool:
        """
        The normal Command.can_run but it ignores cooldowns.

        Args:
            ctx (commands.Context): The command we want to chek if can be run.

        Returns:
            bool: Whether or not the command can be run.
        """

        if self.ignore_checks_in_help:
            return True
        try:
            return await super().can_run(ctx)
        except commands.CommandOnCooldown:
            return True
