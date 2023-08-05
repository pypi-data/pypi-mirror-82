"""
weitersager.irc
~~~~~~~~~~~~~~~

Internet Relay Chat

:Copyright: 2007-2020 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from typing import Any, Dict, List, Optional, Union

from irc.bot import ServerSpec, SingleServerIRCBot
from jaraco.stream.buffer import LenientDecodingLineBuffer

from .config import IrcChannel, IrcConfig, IrcServer
from .signals import channel_joined, shutdown_requested
from .util import log, start_thread


class Bot(SingleServerIRCBot):
    """An IRC bot to forward messages to IRC channels."""

    def __init__(
        self,
        server: IrcServer,
        nickname: str,
        realname: str,
        channels: List[IrcChannel],
        *,
        shutdown_predicate=None,
    ) -> None:
        log('Connecting to IRC server {0.host}:{0.port:d} ...', server)

        server_spec = ServerSpec(server.host, server.port, server.password)
        SingleServerIRCBot.__init__(self, [server_spec], nickname, realname)

        if server.rate_limit is not None:
            log(
                'IRC send rate limit set to {:.2f} messages per second.',
                server.rate_limit,
            )
            self.connection.set_rate_limit(server.rate_limit)
        else:
            log('No IRC send rate limit set.')

        # Avoid `UnicodeDecodeError` on non-UTF-8 messages.
        self.connection.buffer_class = LenientDecodingLineBuffer

        # Note: `self.channels` already exists in super class.
        self.channels_to_join = channels

        self.shutdown_predicate = shutdown_predicate

    def start(self) -> None:
        """Connect to the server, in a separate thread."""
        start_thread(super().start, self.__class__.__name__)

    def get_version(self):
        return 'Weitersager'

    def on_welcome(self, conn, event) -> None:
        """Join channels after connect."""
        log('Connected to {}:{:d}.', *conn.socket.getpeername())

        channel_names = sorted(c.name for c in self.channels_to_join)
        log('Channels to join: {}', ', '.join(channel_names))

        for channel in self.channels_to_join:
            log('Joining channel {} ...', channel.name)
            conn.join(channel.name, channel.password or '')

    def on_nicknameinuse(self, conn, event) -> None:
        """Choose another nickname if conflicting."""
        self._nickname += '_'
        conn.nick(self._nickname)

    def on_join(self, conn, event) -> None:
        """Successfully joined channel."""
        joined_nick = event.source.nick
        channel_name = event.target

        if joined_nick == self._nickname:
            log('Joined IRC channel: {}', channel_name)
            channel_joined.send(channel_name=channel_name)

    def on_badchannelkey(self, conn, event) -> None:
        """Channel could not be joined due to wrong password."""
        channel = event.arguments[0]
        log('Cannot join channel {} (bad key).', channel)

    def on_privmsg(self, conn, event) -> None:
        """React on private messages."""
        nickmask = event.source
        text = event.arguments[0]
        if self.shutdown_predicate and self.shutdown_predicate(nickmask, text):
            self.shutdown(nickmask)

    def shutdown(self, nickmask: str) -> None:
        """Shut the bot down."""
        log('Shutdown requested by {}.', nickmask)
        shutdown_requested.send()
        self.die('Shutting down.')  # Joins IRC bot thread.

    def say(
        self,
        sender: Optional[Any],
        *,
        channel_name: Optional[str] = None,
        text: Optional[str] = None,
    ) -> None:
        """Say message on channel."""
        self.connection.privmsg(channel_name, text)


class DummyBot:
    def __init__(self, channels: List[IrcChannel]) -> None:
        self.channels = channels

    def start(self) -> None:
        # Fake channel joins.
        for channel in self.channels:
            channel_joined.send(channel_name=channel.name)

    def say(
        self, sender: Optional[Any], *, channel_name=None, text=None
    ) -> None:
        log('{}> {}', channel_name, text)


def create_bot(
    config: IrcConfig, **options: Dict[str, Any]
) -> Union[Bot, DummyBot]:
    """Create and return an IRC bot according to the configuration."""
    if config.server is None:
        log('No IRC server specified; will write to STDOUT instead.')
        return DummyBot(config.channels)

    return Bot(
        config.server,
        config.nickname,
        config.realname,
        config.channels,
        **options,
    )


def default_shutdown_predicate(nickmask: str, text: str) -> bool:
    """Determine if this is a valid shutdown request."""
    return text == 'shutdown!'
