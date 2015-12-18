foo = ->
  try
    yield 'B'
  catch err
    console.log 'error caught inside *foo():', err
  yield 'C'
  throw 'D'

bar = ->
  yield 'A'
  try
    yield from foo()
  catch err
    console.log 'error caught inside *bar():', err
  yield 'E'
  yield from baz()
  yield 'G'

baz = ->
  throw 'F'

it = bar()
console.log 'outside:', it.next().value
console.log 'outside:', it.next(1).value
console.log 'outside:', it.throw(2).value
console.log 'outside:', it.next(3).value

try
  console.log 'outside:', it.next(4).value
catch e
  console.log 'error caught outside:' ,e
