import time
import uuid

from omega_client.communication.single_client_omega_connection import \
    configure_single_client_omega_connection
from omega_client.messaging.common_types import AccountCredentials, AccountInfo
from omega_client.messaging.printing_response_handler import \
    PrintingResponseHandler

OMEGA_ENDPOINT = "tcp://0.0.0.0:9999"
OMEGA_SERVER_KEY = "omega_server_key"
DISTRIBUTED_CLIENTS = False


def main():
    # The client_id is the id assigned by Fund3.  It is unique
    # per client and one client can have multiple accounts (denoted by
    # account_id).
    client_id = 1
    # Sender comp id is a uuid unique to each machine a client uses to identify
    # the machine and to route the appropriate responses back to the machine
    # that sent the request.
    sender_comp_id = str(uuid.uuid4())

    # configure_single_client_omega_connection sets up a default TesConnection
    # with one default client_id
    # The ResponseHandler is a command dispatch callback class.  Basically,
    # when the response is received from Omega, TesConnection will route it to
    # ResponseReceiver, and the type of the response will be determined.
    # Each type of response will trigger a specific function that can be
    # overridden in a child class of ResponseHandler for client designated
    # action upon receiving a certain type of response.  E.g. updating
    # internal order status when ExecutionReport is received, updating
    # balance when balance is received etc.

    # See omega_client.messaging.response_handler and
    # omega_client.messaging.printing_response_handler (example child class
    # that just prints everything).
    omega_connection = configure_single_client_omega_connection(
        omega_endpoint=OMEGA_ENDPOINT,
        omega_server_key=OMEGA_SERVER_KEY,
        client_id=client_id,
        sender_comp_id=sender_comp_id,
        response_handler=PrintingResponseHandler())
    # Starting the TesConnection thread.
    omega_connection.start()
    # Waiting for the TesConnection to be set up.
    omega_connection.wait_until_running()

    # Account id is assigned by Fund3 and is unique per exchange account.
    account_id = 2
    # exchange API credentials
    api_key = "api_key"
    secret_key = "secret_key"
    passphrase = "passphrase"  # Optional, only for certain exchanges.
    # Set up AccountCredentials object.
    credentials = AccountCredentials(account_info=AccountInfo(account_id),
                                     api_key=api_key,
                                     secret_key=secret_key,
                                     passphrase=passphrase)

    # Send logon message, which when received will start and update token for
    # session_refresher. session_refresher will run until stopped
    omega_connection.logon([credentials])
    time.sleep(2)

    # send a heartbeat every minute for 2 hours (during which the session
    # should refresh at least once)
    minutes_left = 120
    while minutes_left > 0:
        omega_connection.send_heartbeat()
        time.sleep(60)

    # stop and cleanup
    omega_connection.logoff()
    time.sleep(2)
    omega_connection.cleanup()


if __name__ == '__main__':
    main()
