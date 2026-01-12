import hashlib
import subprocess
import time
import os
from dataset import *
import proto_pb2
import proto_pb2_grpc
import grpc

grpc_server_proc = None

if os.path.exists("go/bin/perftest"):
    go_bin_path = "go/bin/perftest"
if os.path.exists("./../go/bin/perftest"):
    go_bin_path = "./../go/bin/perftest"

def start_grpc_server():
    global grpc_server_proc
    if not grpc_server_proc:
        grpc_server_proc = subprocess.Popen(
            [go_bin_path, 'grpc'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        time.sleep(1)
        # if the server is running - all ok
        if grpc_server_proc.poll() == 0:
            raise Exception(f"Failed starting GRPC server: \n"
                        f"{grpc_server_proc.stdout.read(1000).decode()} "
                        f"{grpc_server_proc.stderr.read(1000).decode()} ")


def proc_count_words(string:str):
    start_grpc_server()
    with grpc.insecure_channel("unix:///tmp/python_go_perftest.sock") as channel:
        # Create a stub (client)
        stub = proto_pb2_grpc.PerftestStub(channel)

        chunkSize = 1024 * 1024
        sLen = len(string)
        if sLen > chunkSize:
            # Call RPC
            def str_message_generator():
                for i in range(0, sLen, chunkSize):
                    yield proto_pb2.StringRequest(content=string[i:i+chunkSize])
            response = stub.CountWordsStream(str_message_generator())
            return response.value
        else:
            response = stub.CountWords(proto_pb2.StringRequest(content=string))
            return response.value