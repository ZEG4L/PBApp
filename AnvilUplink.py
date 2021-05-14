import anvil.server
from slack_sdk import WebClient
anvil.server.connect("UplinkCode")

@anvil.server.callable
def webclient(token):
  client = WebClient(token=token)
  return client

anvil.server.wait_forever()