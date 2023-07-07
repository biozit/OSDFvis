import json
import time
import requests
import logging

class MaddashClient:
  def __init__(self, conf):
    self.conf = conf

  def post(self, transferTest, rate) -> None:
    url = "https://perfsonar.nrp-nautilus.io/esmond/perfsonar/archive/"
    key = "b2db078330ffd141effb6e5253a77ae75b6cd974"
    headers = {'Content-Type': "application/json",'Authorization': "Token {}".format(key)}


    payload = {
      "subject-type": "point-to-point",
      "source": transferTest.sourceIP,
      "destination": transferTest.destinationIP,
      "tool-name": 'xrootd',
      "measurement-agent": transferTest.sourceIP,
      "input-source": transferTest.source,
      "input-destination": transferTest.destination,
      "event-types": [{"event-type": "throughput","summaries":[{"summary-type": "aggregation","summary-window": 60},{"summary-type": "aggregation","summary-window": 60}]}]
      #"event-types": [{"event-type": "throughput","summaries":[{"summary-type": "aggregation","summary-window": 3600},{"summary-type": "aggregation","summary-window": 86400}]}]
      #"event-types": [{"event-type": "throughput","summaries":[{"summary-type": "average","summary-window": 10}]}]
    }

    m = requests.post(url, data=json.dumps(payload), headers=headers)
    print(m)
    print(json.dumps(payload))
    returnJSON = m.json()
    metadataKey = returnJSON['metadata-key']
    urls = returnJSON['url']
    dat = {
        "ts": int(time.time()),
        "val": rate[0]
    }
    urls = urls + 'throughput/base'
    print(json.dumps(dat))
    print(headers)
    print(urls)
    r = requests.post(urls, data=json.dumps(dat), headers=headers)
    print("------------------- "+ urls)
    print(r)
