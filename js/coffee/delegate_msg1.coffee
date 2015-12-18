bar = ->
  console.log "inside '*bar()':", yield 'A'
  console.log "inside '*bar()':", yield from ['B', 'C', 'D']
  console.log "inside '*bar()':", yield 'E'
  'F'

it = bar()
console.log 'outside:', it.next().value
console.log 'outside:', it.next(1).value
console.log 'outside:', it.next(2).value
console.log 'outside:', it.next(3).value
console.log 'outside:', it.next(4).value
console.log 'outside:', it.next(5).value
