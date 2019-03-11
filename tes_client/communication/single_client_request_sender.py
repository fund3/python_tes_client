from queue import Queue
from typing import List

import zmq

from tes_client.messaging.common_types import AccountCredentials, AccountInfo, \
    Order, OrderInfo, OrderType, RequestHeader, TimeInForce
from tes_client.communication.request_sender import RequestSender


class SingleClientRequestSender:
    """
    Wrapper around RequestSender with added boilerplate code support use cases
    with only 1 client_id.
    """
    def __init__(self, zmq_context: zmq.Context,
                 connection_string: str,
                 client_id: int,
                 sender_comp_id: str,
                 outgoing_message_queue: Queue = None):
        self._request_sender = RequestSender(
            zmq_context=zmq_context,
            zmq_endpoint=connection_string,
            outgoing_message_queue=outgoing_message_queue)
        self._request_header = RequestHeader(client_id=client_id,
                                             sender_comp_id=sender_comp_id,
                                             access_token='',
                                             request_id=0)
        # TODO (low priority) change _request_header to use variable request_id
        # client should override self._request_header in their implementation
        #  and use their own method for generating request_ids

    def set_access_token(self, access_token: str):
        """
        Sets the access_token in self._request_header.
        :param access_token: (str) Access token granted by TES.  Note that
            access_token is ignored in logon.
        """
        self._request_header.access_token = access_token

    def start(self):
        self._request_sender.start()

    def stop(self):
        self._request_sender.stop()

    def is_running(self):
        """
        Return True if the RequestSender is running, False otherwise.
        """
        return self._request_sender.is_running()

    def cleanup(self):
        self._request_sender.cleanup()
    """
    ############################################################################

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Outgoing TESMessages ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ----------------- Public Methods to be called by client -------------------

    ############################################################################
    """
    def logon(self,
              client_secret: str,
              credentials: List[AccountCredentials]):
        return self._request_sender.logon(
            request_header=self._request_header,
            client_secret=client_secret,
            credentials=credentials)

    def logoff(self):
        return self._request_sender.logoff(request_header=self._request_header)

    def send_heartbeat(self):
        return self._request_sender.send_heartbeat(
            request_header=self._request_header)

    def request_server_time(self):
        return self._request_sender.request_server_time(
            request_header=self._request_header)

    def place_order(self, order: Order):
        return self._request_sender.place_order(
            request_header=self._request_header, order=order)

    def replace_order(self, account_info: AccountInfo,
                      order_id: str,
                      order_type: str=OrderType.market.name,
                      quantity: float = 0.0,
                      price: float = 0.0,
                      stop_price: float = 0.0,
                      time_in_force: str = TimeInForce.gtc.name,
                      expire_at: float = 0.0):
        return self._request_sender.replace_order(
            request_header=self._request_header,
            account_info=account_info,
            order_id=order_id,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
            time_in_force=time_in_force,
            expire_at=expire_at
        )

    def cancel_order(self, account_info: AccountInfo,
                     order_id: str):
        return self._request_sender.cancel_order(
            request_header=self._request_header,
            account_info=account_info,
            order_id=order_id)

    def request_account_data(self, account_info: AccountInfo):
        return self._request_sender.request_account_data(
            request_header=self._request_header, account_info=account_info)

    def request_open_positions(self, account_info: AccountInfo):
        return self._request_sender.request_open_positions(
            request_header=self._request_header, account_info=account_info)

    def request_account_balances(self, account_info: AccountInfo):
        return self._request_sender.request_account_balances(
            request_header=self._request_header, account_info=account_info)

    def request_working_orders(self, account_info: AccountInfo):
        return self._request_sender.request_working_orders(
            request_header=self._request_header, account_info=account_info)

    def request_order_status(self, account_info: AccountInfo,
                             order_id: str):
        return self._request_sender.request_order_status(
            request_header=self._request_header,
            account_info=account_info,
            order_id=order_id)

    def request_completed_orders(self, account_info: AccountInfo,
                                 count: int = None,
                                 since: float = None):
        return self._request_sender.request_completed_orders(
            request_header=self._request_header,
            account_info=account_info,
            count=count,
            since=since)

    def request_exchange_properties(self, exchange: str):
        return self._request_sender.request_exchange_properties(
            request_header=self._request_header, exchange=exchange)