import system

args = [
  "1000 1",
  "1000 200",
  "1000 400",
  "1000 600",
  "1000 800",
  "1200 1",
  "1200 200",
  "1200 400",
  "1200 600",
  "1200 800",
  "1200 1000",
  "1400 1",
  "1400 200",
  "1400 400",
  "1400 600",
  "1400 800",
  "1400 1000",
  "1400 1200",
  "1600 1",
  "1600 200",
  "1600 400",
  "1600 600",
  "1600 800",
  "1600 1000",
  "1600 1200",
  "1600 1400",
  "1800 1",
  "1800 200",
  "1800 400",
  "1800 600",
  "1800 800",
  "1800 1000",
  "1800 1200",
  "1800 1400",
  "1800 1600",
  "2000 1",
  "2000 200",
  "2000 400",
  "2000 600",
  "2000 800",
  "2000 1000",
  "2000 1200",
  "2000 1400",
  "2000 1600",
  "2000 1800",
]

for arg in args:
  system("python filename.py " + arg) 
