# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
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

"""This module contains tests for transaction."""
from unittest.mock import patch

import pytest

from aea.helpers.transaction.base import (
    RawMessage,
    RawTransaction,
    SignedMessage,
    SignedTransaction,
    Terms,
)
from aea.protocols.signing.message import SigningMessage

from tests.conftest import COSMOS


class TestSigningMessage:
    """Test the signing message module."""

    @classmethod
    def setup_class(cls):
        """Setup class for test case."""
        cls.ledger_id = COSMOS
        cls.terms = Terms(
            ledger_id=cls.ledger_id,
            sender_address="address1",
            counterparty_address="address2",
            amount_by_currency_id={"FET": -2},
            quantities_by_good_id={"good_id": 10},
            is_sender_payable_tx_fee=True,
            nonce="transaction nonce",
        )

    def test_sign_transaction(self):
        """Test for an error for a sign transaction message."""
        tx_msg = SigningMessage(
            performative=SigningMessage.Performative.SIGN_TRANSACTION,
            terms=self.terms,
            raw_transaction=RawTransaction(self.ledger_id, "transaction"),
        )
        assert tx_msg._is_consistent()
        encoded_tx_msg = tx_msg.encode()
        decoded_tx_msg = tx_msg.serializer.decode(encoded_tx_msg)
        assert tx_msg == decoded_tx_msg

    def test_sign_message(self):
        """Test for an error for a sign transaction message."""
        tx_msg = SigningMessage(
            performative=SigningMessage.Performative.SIGN_MESSAGE,
            terms=self.terms,
            raw_message=RawMessage(self.ledger_id, "message"),
        )
        assert tx_msg._is_consistent()
        encoded_tx_msg = tx_msg.encode()
        decoded_tx_msg = tx_msg.serializer.decode(encoded_tx_msg)
        assert tx_msg == decoded_tx_msg

    def test_signed_transaction(self):
        """Test for an error for a signed transaction."""
        tx_msg = SigningMessage(
            performative=SigningMessage.Performative.SIGNED_TRANSACTION,
            message_id=2,
            target=1,
            signed_transaction=SignedTransaction(self.ledger_id, "signature"),
        )
        assert tx_msg._is_consistent()
        encoded_tx_msg = tx_msg.encode()
        decoded_tx_msg = tx_msg.serializer.decode(encoded_tx_msg)
        assert tx_msg == decoded_tx_msg

    def test_signed_message(self):
        """Test for an error for a signed message."""
        tx_msg = SigningMessage(
            performative=SigningMessage.Performative.SIGNED_MESSAGE,
            message_id=2,
            target=1,
            signed_message=SignedMessage(self.ledger_id, "message"),
        )
        assert tx_msg._is_consistent()
        encoded_tx_msg = tx_msg.encode()
        decoded_tx_msg = tx_msg.serializer.decode(encoded_tx_msg)
        assert tx_msg == decoded_tx_msg

    def test_error_message(self):
        """Test for an error for an error message."""
        tx_msg = SigningMessage(
            performative=SigningMessage.Performative.ERROR,
            message_id=2,
            target=1,
            error_code=SigningMessage.ErrorCode.UNSUCCESSFUL_MESSAGE_SIGNING,
        )
        assert tx_msg._is_consistent()
        encoded_tx_msg = tx_msg.encode()
        decoded_tx_msg = tx_msg.serializer.decode(encoded_tx_msg)
        assert tx_msg == decoded_tx_msg
        assert str(tx_msg.performative) == "error"
        assert len(tx_msg.valid_performatives) == 5


def test_consistency_check_negative():
    """Test the consistency check, negative case."""
    tx_msg = SigningMessage(performative=SigningMessage.Performative.SIGN_TRANSACTION,)
    assert not tx_msg._is_consistent()


def test_serialization_negative():
    """Test serialization when performative is not recognized."""
    tx_msg = SigningMessage(
        performative=SigningMessage.Performative.ERROR,
        message_id=2,
        target=1,
        error_code=SigningMessage.ErrorCode.UNSUCCESSFUL_MESSAGE_SIGNING,
    )

    with patch.object(SigningMessage.Performative, "__eq__", return_value=False):
        with pytest.raises(
            ValueError, match=f"Performative not valid: {tx_msg.performative}"
        ):
            tx_msg.serializer.encode(tx_msg)

    encoded_tx_bytes = tx_msg.serializer.encode(tx_msg)
    with patch.object(SigningMessage.Performative, "__eq__", return_value=False):
        with pytest.raises(
            ValueError, match=f"Performative not valid: {tx_msg.performative}"
        ):
            tx_msg.serializer.decode(encoded_tx_bytes)
