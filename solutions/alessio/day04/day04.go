package main

import (
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func searchWord(r int, c int, mat []string, rows int, cols int) int {
	dirs := [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}}
	letters := "MAS"

	cnt := 0
	for _, dir := range dirs {
		match := true
		for i := range len(letters) {
			next_r := r + (i+1)*dir[0]
			next_c := c + (i+1)*dir[1]
			if next_r < 0 || next_c < 0 || next_r >= rows || next_c >= cols || mat[next_r][next_c] != letters[i] {
				match = false
				break
			}
		}
		if match {
			cnt++
		}
	}

	return cnt
}

func part1(lines []string) {
	rows := len(lines)
	cols := len(lines[0])
	cnt := 0

	for r := range rows {
		for c := range cols {
			if lines[r][c] == 'X' {
				cnt += searchWord(r, c, lines, rows, cols)
			}
		}
	}

	fmt.Println(cnt)
}

func searchXMas(r int, c int, mat []string) int {
	diag11 := mat[r-1][c-1] == 'M' && mat[r+1][c+1] == 'S'
	diag12 := mat[r-1][c-1] == 'S' && mat[r+1][c+1] == 'M'
	diag21 := mat[r-1][c+1] == 'M' && mat[r+1][c-1] == 'S'
	diag22 := mat[r-1][c+1] == 'S' && mat[r+1][c-1] == 'M'

	if (diag11 || diag12) && (diag21 || diag22) {
		return 1
	}

	return 0
}

func part2(lines []string) {
	rows := len(lines)
	cols := len(lines[0])
	cnt := 0

	for r := 1; r < rows-1; r++ {
		for c := 1; c < cols-1; c++ {
			if lines[r][c] == 'A' {
				cnt += searchXMas(r, c, lines)
			}
		}
	}

	_, err := fmt.Println(cnt)
	check(err)
}
func main() {
	data, err := os.ReadFile("./input04.txt")
	check(err)

	lines := strings.Split(strings.Trim(string(data), "\r\n"), "\r\n")

	part1(lines)
	part2(lines)
}
