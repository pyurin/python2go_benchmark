package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	pb "perftest/perftest/proto"

	"google.golang.org/grpc"
)

/**
	GRPC interaction:
 		 - server
		 - rpc handling
*/

type perftestServer struct {
	pb.PerftestServer
}

// CountWords
// straightforward rpc
func (s *perftestServer) CountWords(ctx context.Context, stringRequest *pb.StringRequest) (*pb.IntResponse, error) {
	return &pb.IntResponse{Value: int64(countWords(stringRequest.Content))}, nil
}

// CountWordsStream
// Handle streaming rpc request w/o chunked processing.
// (tested chunked processing, does not give much CPU improvement)
func (s *perftestServer) CountWordsStream(srv grpc.ClientStreamingServer[pb.StringRequest, pb.IntResponse]) error {
	var str string

	for {
		streamBuf, err := srv.Recv()
		if err == io.EOF {
			return srv.SendAndClose(&pb.IntResponse{Value: int64(countWords(str))})
		}
		if err != nil {
			return err
		}
		str += streamBuf.Content
	}
}

func StartGRPCServer() {
	sock := "/tmp/python_go_perftest.sock"
	_ = os.Remove(sock)

	lis, err := net.Listen("unix", sock)
	if err != nil {
		panic(fmt.Sprint("listen: %v", err))
	}

	s := grpc.NewServer()
	pb.RegisterPerftestServer(s, &perftestServer{})
	// pb.RegisterMyServiceServer(s, &impl{})

	log.Printf("listening on unix://%s", sock)
	s.Serve(lis)
}
