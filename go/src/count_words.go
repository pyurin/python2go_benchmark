package main

// countWords
// wount words in a string
func countWords(str string) int {
	wordCount := 0
	strlen := len(str)
	for i := 0; i < strlen; i++ {
		chr := str[i]
		if chr != ' ' && chr != '\n' && chr != '\r' { // a word started
			wordCount++
			for ; i < strlen && str[i] != ' ' && str[i] != '\n' && str[i] != '\r'; i++ { // read a word
				continue
			}
		}
	}
	return wordCount
}
