package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"slices"
)

/*
	Pipe interaction.
	As pipes are streamed by designe, there are at least several ways how to read them:
 		- entirely
		- chunked
		- chunked with bufio.Scanner
*/

// CountWordsPipe
// Read pipe entirely and process
func CountWordsPipe() {
	bytes, _ := io.ReadAll(os.Stdin)
	str := string(bytes)
	wordCount := countWords(str)
	fmt.Printf("%d", wordCount)
}

// CountWordsPipeChunked
// Read pipe using 64k buffer and process chunks,
// chunks are aligned with [" \n\r"] characters
func CountWordsPipeChunked() {
	readOverflowBuf := []byte{}
	readBuf := make([]byte, 64*1024) // buf must be larger than 1
	wordCount := 0
	for {
		readLen, readErr := os.Stdin.Read(readBuf)
		if readLen > 0 && readErr == nil {
			//fmt.Print("Read bytes: ", readBuf[:readLen], " as str: ", string(readBuf[:readLen]), "\n")
			i2 := readLen - 1
			for ; i2 > 0; i2-- {
				//fmt.Print("Checking byte: ", readBuf[i2], "\n")
				if readBuf[i2] == ' ' {
					//fmt.Print("Truncated string to: ", readBuf[:i2], " as str: ", string(readBuf[:i2]), "\n")
					stringBuf := slices.Concat(readOverflowBuf, readBuf[:i2])
					//fmt.Print("String buf is ", stringBuf, ", as string: ", string(stringBuf), "\n")
					wordCount += countWords(string(stringBuf))
					//fmt.Print("Word count updated to ", wordCount, "\n")
					readOverflowBuf = readOverflowBuf[:0]
					break
				}
			}
			//fmt.Print("Buf read finished, i2 = ", i2, " and readLen = ", readLen, "\n")
			overflowLen := readLen - i2
			if overflowLen > 0 {
				readOverflowBuf = slices.Concat(readOverflowBuf, readBuf[readLen-overflowLen:readLen])
				//fmt.Print("Should save overflow of ", overflowLen, " bytes, overflow = ", readOverflowBuf, "\n")
			}
		}
		if readErr != nil {
			if readErr == io.EOF {
				//fmt.Print("EOF reached, flushing bufs: ", readOverflowBuf, readBuf[:readLen], "\n")
				stringBuf := slices.Concat(readOverflowBuf, readBuf[:readLen])
				wordCount += countWords(string(stringBuf))
				//fmt.Print("Word count updated to ", wordCount, "\n")
				break
			} else {
				panic(fmt.Sprint("Error reading from stdin: ", readErr))
			}
		}
	}
	fmt.Printf("%d", wordCount)
}

// CountWordsPipeWithScanner
// Read pipe with bufio.ScanWords scanner
func CountWordsPipeWithScanner() {
	var wordCount int
	// read from stdin, count interatively, return to stdout
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Split(bufio.ScanWords)
	for scanner.Scan() {
		wordCount++
		//line := scanner.Text()
		//fmt.Println("Got:", line)
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
	fmt.Printf("%d", wordCount)
}
