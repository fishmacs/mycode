MAX_VALUE = 4

counter = (max = MAX_VALUE) =>
  i = 0
  for i in [1..max]
    console.log i
  console.log 'at last...', i

counter()
