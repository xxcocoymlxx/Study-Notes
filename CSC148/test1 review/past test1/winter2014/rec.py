def rec(a: int, b: int) -> int:
  if a + b <= 0:
    return 1
  return rec(a - 1, b) + rec(a - 1, b - 1)
  
print(rec(2, 2))
