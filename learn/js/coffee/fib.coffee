i = 0

fibonacci = (n) ->
  i++
  if n > 1 then fibonacci(n-2) + fibonacci(n-1) else n
    
    
for x in [0..10]
  fib x

for x in [0..10]
  fib x
q  
