#!/bin/bash
set -e -o pipefail

echo -e "\n######### Generating Python GRPC\n"
uv run --project=./python/ -m grpc_tools.protoc -I=./grpc/ --grpc_python_out=./python/src/ --python_out=./python/src/ proto.proto

echo -e "\n######### Generating Go GRPC\n"
protoc --go_out=./go/src/ --go-grpc_out=./go/src/ ./grpc/proto.proto

echo -e "\n######### Building app\n"
go build -C ./go/src/ -o ./../bin/

echo -e "\n######### Building shared lib\n"
go build -C ./go/src/ --buildmode=c-shared  -o ./../bin/perftest.so