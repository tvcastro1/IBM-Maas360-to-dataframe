from dotenv import load_dotenv
from endpoints import AUTH_ENDPOINT
import os
import requests
import xml.etree.ElementTree as ET

load_dotenv()
PLATAFORM_ID = 3
BILLING_ID = os.environ.get("BILLING_ID")
PASSWORD = os.environ.get("PASSWORD")
USERNAME = os.environ.get("USERNAME")
APP_ID = os.environ.get("APP_ID")
APP_VERSION = os.environ.get("APP_VERSION")
APP_ACCESS_KEY = os.environ.get("APP_ACCESS_KEY")


xml_payload = """<authRequest>
    <maaS360AdminAuth>
        <platformID>{}</platformID>
        <billingID>{}</billingID>
        <password>{}</password>
        <userName>{}</userName>
        <appID>{}</appID>
        <appVersion>{}</appVersion>
        <appAccessKey>{}</appAccessKey>
    </maaS360AdminAuth>
</authRequest>""".format(
    PLATAFORM_ID, BILLING_ID, PASSWORD, USERNAME, APP_ID, APP_VERSION, APP_ACCESS_KEY
)

headers = {"Content-Type": "application/xml; charset=utf-8"}


def extract_auth_token(xml_response):
    """Extract the authToken from the XML response.

    Args:
        xml_response (str): The XML response from the authentication API.

    Returns:
        str: The extracted authToken.
    """
    root = ET.fromstring(xml_response)
    return root.find("authToken").text


def auth():
    """Authenticate to the MaaS360 API and get the authToken.

    Returns:
        str: The authToken.
    """
    response = requests.post(AUTH_ENDPOINT, data=xml_payload, headers=headers)
    auth_token = extract_auth_token(response.text)
    return auth_token


if __name__ == "__main__":
    auth_token = auth()
    print(auth_token)
