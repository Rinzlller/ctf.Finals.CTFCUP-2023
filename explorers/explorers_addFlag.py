#!/usr/bin/env python3

import requests
import random
import string
import ua_generator
import re
import sys
import json


port = 8000
flag_regexp = re.compile(r'[A-Z0-9]{31}=')


class Standart_User:
    def __init__(self, ip):
        self.host = f"http://{ip}:{port}"
        self.session = requests.Session()
        self.session.headers = {"User-agent": ua_generator.generate().text}

        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        self.username = random_string
        self.password = random_string
        self.flag = f"{''.join(random.choice(string.ascii_letters + string.digits).upper() for _ in range(31))}="

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
                "description": self.flag
            }
        )
        return resp.text
            
    
def main():

    try:
        ip = sys.argv[1]
    except:
        print(f"USAGE:\t{sys.argv[0]} <victim-ip-address>")
        sys.exit(1)

    for _ in range(5):
        flagholder = Standart_User(ip)
        resp = flagholder.create_route()
        print( json.loads(resp)["id"] )
    

if __name__ == "__main__":
    main()