import sys
import n2yo_api

passes = n2yo_api.retrieve_satelite(int(sys.argv[1]), True, False, False, 1, 43.484443, 5.417168)
next_pass = passes[0]

print(next_pass["start"]["utc"], end=" ")
print(next_pass["end"]["utc"]-next_pass["start"]["utc"], end=" ")
print(int(next_pass["max"]["elevation"]))
