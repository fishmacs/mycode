foo = ->
  console.log "inside '*foo()':", yield 'B'
  console.log "inside '*foo()':", yield 'C'
  'D'

bar = ->
  console.log "inside '*bar()':", yield 'A'
  console.log "inside '*bar()':", yield from foo()
  console.log "inside '*bar()':", yield 'E'
  'F'

it = bar()
console.log 'outside:', it.next().value
console.log 'outside:', it.next(1).value
console.log 'outside:', it.next(2).value
console.log 'outside:', it.next(3).value
console.log 'outside:', it.next(4).value
