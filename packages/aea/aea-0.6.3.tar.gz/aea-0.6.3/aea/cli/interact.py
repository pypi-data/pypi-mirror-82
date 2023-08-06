# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Implementation of the 'aea interact' subcommand."""

import codecs
from pathlib import Path
from typing import Optional, Union

import click

from aea.cli.utils.decorators import check_aea_project
from aea.cli.utils.exceptions import InterruptInputException
from aea.common import Address
from aea.configurations.base import (
    ConnectionConfig,
    DEFAULT_AEA_CONFIG_FILE,
    PackageType,
)
from aea.configurations.loader import ConfigLoader
from aea.connections.stub.connection import (
    DEFAULT_INPUT_FILE_NAME,
    DEFAULT_OUTPUT_FILE_NAME,
    StubConnection,
)
from aea.identity.base import Identity
from aea.mail.base import Envelope, Message
from aea.multiplexer import InBox, Multiplexer, OutBox
from aea.protocols.default.dialogues import DefaultDialogue, DefaultDialogues
from aea.protocols.default.message import DefaultMessage
from aea.protocols.dialogue.base import Dialogue as BaseDialogue


@click.command()
@click.pass_context
@check_aea_project
def interact(click_context: click.core.Context):  # pylint: disable=unused-argument
    """Interact with a running AEA via the stub connection."""
    click.echo("Starting AEA interaction channel...")
    _run_interaction_channel()


def _run_interaction_channel():
    # load agent configuration file
    loader = ConfigLoader.from_configuration_type(PackageType.AGENT)
    agent_configuration = loader.load(Path(DEFAULT_AEA_CONFIG_FILE).open())
    agent_name = agent_configuration.name
    # load stub connection
    configuration = ConnectionConfig(
        input_file=DEFAULT_OUTPUT_FILE_NAME,
        output_file=DEFAULT_INPUT_FILE_NAME,
        connection_id=StubConnection.connection_id,
    )
    identity_stub = Identity(agent_name + "_interact", "interact")
    stub_connection = StubConnection(
        configuration=configuration, identity=identity_stub
    )
    multiplexer = Multiplexer([stub_connection])
    inbox = InBox(multiplexer)
    outbox = OutBox(multiplexer)

    def role_from_first_message(  # pylint: disable=unused-argument
        message: Message, receiver_address: Address
    ) -> BaseDialogue.Role:
        """Infer the role of the agent from an incoming/outgoing first message

        :param message: an incoming/outgoing first message
        :param receiver_address: the address of the receiving agent
        :return: The role of the agent
        """
        return DefaultDialogue.Role.AGENT

    dialogues = DefaultDialogues(identity_stub.name, role_from_first_message)

    try:
        multiplexer.connect()
        while True:  # pragma: no cover
            _process_envelopes(agent_name, inbox, outbox, dialogues)

    except KeyboardInterrupt:
        click.echo("Interaction interrupted!")
    except BaseException as e:  # pylint: disable=broad-except # pragma: no cover
        click.echo(e)
    finally:
        multiplexer.disconnect()


def _process_envelopes(
    agent_name: str, inbox: InBox, outbox: OutBox, dialogues: DefaultDialogues,
) -> None:
    """
    Process envelopes.

    :param agent_name: name of an agent.
    :param inbox: an inbox object.
    :param outbox: an outbox object.
    :param dialogues: the dialogues object.

    :return: None.
    """
    envelope = _try_construct_envelope(agent_name, dialogues)
    if envelope is None:
        _check_for_incoming_envelope(inbox)
    else:
        outbox.put(envelope)
        click.echo(_construct_message("sending", envelope))


def _check_for_incoming_envelope(inbox: InBox):
    if not inbox.empty():
        envelope = inbox.get_nowait()
        if envelope is None:
            raise ValueError("Could not recover envelope from inbox.")
        click.echo(_construct_message("received", envelope))
    else:
        click.echo("Received no new envelope!")


def _construct_message(action_name: str, envelope: Envelope):
    action_name = action_name.title()
    msg = (
        DefaultMessage.serializer.decode(envelope.message)
        if isinstance(envelope.message, bytes)
        else envelope.message
    )
    message = (
        "\n{} envelope:\nto: "
        "{}\nsender: {}\nprotocol_id: {}\nmessage: {}\n".format(
            action_name, envelope.to, envelope.sender, envelope.protocol_id, msg,
        )
    )
    return message


def _try_construct_envelope(
    agent_name: str, dialogues: DefaultDialogues
) -> Optional[Envelope]:
    """Try construct an envelope from user input."""
    envelope = None  # type: Optional[Envelope]
    try:
        performative_str = "bytes"
        performative = DefaultMessage.Performative(performative_str)
        click.echo(
            "Provide message of protocol fetchai/default:0.7.0 for performative {}:".format(
                performative_str
            )
        )
        message_escaped = input()  # nosec
        message_escaped = message_escaped.strip()
        if message_escaped == "":
            raise InterruptInputException
        if performative == DefaultMessage.Performative.BYTES:
            message_decoded = codecs.decode(
                message_escaped.encode("utf-8"), "unicode-escape"
            )
            message = message_decoded.encode("utf-8")  # type: Union[str, bytes]
        else:
            message = message_escaped  # pragma: no cover
        msg, _ = dialogues.create(
            counterparty=agent_name, performative=performative, content=message,
        )
        envelope = Envelope(
            to=msg.to, sender=msg.sender, protocol_id=msg.protocol_id, message=msg,
        )
    except InterruptInputException:
        click.echo("Interrupting input, checking inbox ...")
    except KeyboardInterrupt as e:
        raise e
    except BaseException as e:  # pylint: disable=broad-except # pragma: no cover
        click.echo(e)
    return envelope
