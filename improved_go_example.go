package main

import (
	"fmt"
)

func main() {
	fmt.Println("╔════════════════════════════════════════╗")
	fmt.Println("║   STUDENT GRADE MANAGER SYSTEM         ║")
	fmt.Println("╚════════════════════════════════════════╝")
	fmt.Println()

	var n int
	fmt.Print("Enter number of students: ")
	fmt.Scan(&n)
	fmt.Println() // Add blank line after input

	// Slice to store marks
	marks := make([]int, n)

	// Input marks with better formatting
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("📝 ENTERING STUDENT MARKS")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	
	for i := 0; i < n; i++ {
		fmt.Printf("Student %d marks: ", i+1)
		fmt.Scan(&marks[i])
	}
	fmt.Println() // Blank line after all inputs

	// Calculate total
	total := 0
	for i := 0; i < n; i++ {
		total += marks[i]
	}

	// Average
	avg := float64(total) / float64(n)

	// Find highest & lowest
	high := marks[0]
	low := marks[0]

	for i := 1; i < n; i++ {
		if marks[i] > high {
			high = marks[i]
		}
		if marks[i] < low {
			low = marks[i]
		}
	}

	// Final Report with better formatting
	fmt.Println("╔════════════════════════════════════════╗")
	fmt.Println("║           ANALYSIS REPORT              ║")
	fmt.Println("╚════════════════════════════════════════╝")
	fmt.Println()
	
	fmt.Printf("📊 Total Students     : %d\n", n)
	fmt.Printf("📈 Total Marks        : %d\n", total)
	fmt.Printf("📉 Average Marks      : %.2f\n", avg)
	fmt.Printf("⭐ Highest Marks      : %d\n", high)
	fmt.Printf("⚠️  Lowest Marks       : %d\n", low)
	fmt.Println()

	// Grade based on average
	fmt.Print("🎓 Overall Grade      : ")

	var grade string
	if avg >= 90 {
		grade = "A+ (Excellent!)"
	} else if avg >= 80 {
		grade = "A (Very Good)"
	} else if avg >= 70 {
		grade = "B (Good)"
	} else if avg >= 60 {
		grade = "C (Average)"
	} else if avg >= 50 {
		grade = "D (Below Average)"
	} else {
		grade = "F (Fail - Need Improvement)"
	}
	fmt.Println(grade)
	
	fmt.Println()
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("💡 Keep working hard! Success = Effort 🚀")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
}
