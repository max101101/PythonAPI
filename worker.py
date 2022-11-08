import requests
import sqlite3
import time
import json

import database
import properties

if __name__ == '__main__':
  database.init(sqlite3.connect(properties.db_name))
  conn = sqlite3.connect(properties.db_name)
  conn.row_factory = database.dict_factory

  while True:
    response = requests.request("GET",
      properties.football_api_url,
      headers = properties.football_api_headers,
      params = properties.football_api_querystring)

    r = json.loads(response.text)

    for m in r["response"]: 
      matchid = str(m["fixture"]["id"])
      print("handle match ", matchid)

      notification = database.get_notification(conn, matchid)
      if notification is None:
        database.add_notification(conn, matchid)
        conn.commit()
        notification = {}
        notification["events"] = 0

      if len(m["events"]) <= notification["events"]:
        continue

      for event in m["events"][notification["events"]:]:
        print("\thandle event ", event["time"]["elapsed"])
        if event["type"] == 'Goal' or event["type"] == 'Var':
          fav = database.get_favourites_by_matchid(conn, matchid)
          for f in fav:
            print("\t\tsend notification to  ", f["userid"])
            #send_notification(f["userid"], event)
            pass

      database.update_notification(conn, matchid, len(m["events"]))
      conn.commit()

    time.sleep(properties.worker_sleep_time)
