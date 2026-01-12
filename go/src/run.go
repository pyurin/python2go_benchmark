package main

import (
	"fmt"
	"os"
)

/*
App entrypoint.
Options:

	count_words_pipe - count words from pipe, reading entirely
	count_words_pipe_scanner - count words from pipe, using bufio word scanner
	count_words_pipe_chunked - count words from pipe, reading chunks manually
	grpc - start grpc server and expose rpc
*/
func main() {
	if len(os.Args) > 1 {
		switch os.Args[1] {

		case "count_words_pipe_scanner":
			_, _ = fmt.Fprint(os.Stderr, "Reading pipe with scanner\n")
			CountWordsPipeWithScanner()

		case "count_words_pipe":
			_, _ = fmt.Fprint(os.Stderr, "Reading pipe raw\n")
			CountWordsPipe()

		case "count_words_pipe_chunked":
			_, _ = fmt.Fprint(os.Stderr, "Reading pipe chunked\n")
			CountWordsPipeChunked()

		case "grpc":
			_, _ = fmt.Fprint(os.Stderr, "Starting GRPC\n")
			StartGRPCServer()

		default:
			_, _ = fmt.Fprint(os.Stderr, "Give me a correct argument, please\n")

		}
	} else {
		_, _ = fmt.Fprint(os.Stderr, "Give me an argument, please\n")
	}
}
