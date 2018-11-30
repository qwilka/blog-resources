import json
import logging
import os
#import sys

import requests

logger = logging.getLogger(__name__)


def check_CDP_API_key():
    # https://doc.cognitedata.com/faq/#how-do-i-check-if-my-api-key-is-valid
    apiKey = os.environ.get("COGNITE_API_KEY")
    if not apiKey:
        logger.error("check_CDP_API_key: «COGNITE_API_KEY» must be set as an environment variable!")
        return None
    headers = {
        "Host": "api.cognitedata.com",
        "Content-Type": "application/json",
        "Content-Length": "31",
    }
    payload = {
        'apiKey': apiKey
    }
    req = requests.post("https://api.cognitedata.com/login", headers=headers, data=json.dumps(payload))
    # print("req.status_code: ", req.status_code)
    # print("req.text: ", req.text)
    resp = json.loads(req.text)
    if req.status_code>=400:
        # print(f"ERROR: code={req.status_code} ", end='')
        # if "error" in resp and "message" in resp["error"]:
        #     print(resp["error"]["message"])
        # else:
        #     print("unable to login!")
        msg = resp.get("error", {}).get("message", "unable to login!")
        logger.error("check_CDP_API_key: code=%d «%s»" % (req.status_code, msg))
        return None
    return resp


if __name__=="__main__":
    logger.setLevel(logging.DEBUG)
    lh = logging.StreamHandler()
    logger.addHandler(lh)
    resp = check_CDP_API_key()
    if resp:
        print("«check_CDP_API_key» returned: ", resp)
    else:
        print("login failure indicated by «check_CDP_API_key»!")