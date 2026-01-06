package main

import (
	"fmt"
)

func main() {
	fmt.Println("===== Student Grade Manager =====\n")

	var n int
	fmt.Print("Enter number of students: ")
	fmt.Scan(&n)
	fmt.Printf("✓ Received: %d students\n\n", n)

	// Slice to store marks
	marks := make([]int, n)

	// Input marks
	fmt.Println("Enter marks for each student:")
	for i := 0; i < n; i++ {
		fmt.Printf("  Student %d: ", i+1)
		fmt.Scan(&marks[i])
		fmt.Printf("    ✓ Marks: %d\n", marks[i])
	}

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

	// Final Report
	fmt.Println("\n╔════════════════════════════════════╗")
	fmt.Println("║        ANALYSIS REPORT             ║")
	fmt.Println("╚════════════════════════════════════╝")
	fmt.Printf("\n📊 Total Students  : %d\n", n)
	fmt.Printf("📈 Total Marks     : %d\n", total)
	fmt.Printf("📉 Average Marks   : %.2f\n", avg)
	fmt.Printf("⭐ Highest Marks   : %d\n", high)
	fmt.Printf("⚠️  Lowest Marks    : %d\n", low)

	// Grade based on average
	fmt.Print("\n🎓 Overall Grade   : ")

	if avg >= 90 {
		fmt.Println("A+ (Excellent!)")
	} else if avg >= 80 {
		fmt.Println("A (Very Good)")
	} else if avg >= 70 {
		fmt.Println("B (Good)")
	} else if avg >= 60 {
		fmt.Println("C (Average)")
	} else if avg >= 50 {
		fmt.Println("D (Pass)")
	} else {
		fmt.Println("F (Fail)")
	}

	fmt.Println("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("💪 Keep working hard! Success = Effort 🚀")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
}
