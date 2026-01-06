# Program to calculate sum and average of numbers

cat("Enter 5 numbers:\n")

# Use scan() instead of readline() - it reads from stdin properly
numbers <- scan("stdin", n=5, quiet=TRUE)

cat("\nYou entered:\n")
print(numbers)

total <- sum(numbers)
avg <- mean(numbers)

cat("\nSum =", total, "\n")
cat("Average =", avg, "\n")

# Grade based on average
cat("\nGrade: ")
if (avg >= 90) {
  cat("A+ (Excellent!)\n")
} else if (avg >= 80) {
  cat("A (Very Good)\n")
} else if (avg >= 70) {
  cat("B (Good)\n")
} else if (avg >= 60) {
  cat("C (Average)\n")
} else if (avg >= 50) {
  cat("D (Pass)\n")
} else {
  cat("F (Fail)\n")
}
