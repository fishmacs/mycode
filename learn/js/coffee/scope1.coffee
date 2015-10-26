outer = 1

changeNumbers = ->
  @x = 5
  inner = -1
  outer = 10
  changeInner = ->
    inner = 2

inner = changeNumbers()
console.log outer

do (outer = 5) ->
  x + y
