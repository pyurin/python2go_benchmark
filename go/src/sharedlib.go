package main

/*
#include <stdint.h>
*/
import "C"

// exposed for c-shared lib build, routes call too countWords function
//
//export CountWordsC
func CountWordsC(buf *C.char, bufLen int32) int64 {
	str := C.GoString(buf)
	return int64(countWords(str))
}
