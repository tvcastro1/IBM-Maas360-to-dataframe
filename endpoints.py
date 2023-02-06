import os
from dotenv import load_dotenv


load_dotenv()
BILLING_ID = os.environ.get("BILLING_ID")


AUTH_ENDPOINT = "https://apis.m3.maas360.com/auth-apis/auth/1.0/authenticate/{}".format(
    BILLING_ID
)

DEVICES_ENDPOINT = (
    "https://apis.m3.maas360.com/device-apis/devices/1.0/search/{}".format(BILLING_ID)
)
