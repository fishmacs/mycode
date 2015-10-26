step = (gen) ->
  it = gen()
  last = undefined
  
  ->
    last = it.next(last).value
    return

a = 1
b = 2

foo = ->
  a++
  yield undefined
  b = b * a
  a = (yield b) + 3
  return

bar = ->
  b--
  yield undefined
  a = (yield 8) + b
  b = a * (yield 2)
  return

test = ->
  orders = combine 7, 3
  ret = {}
  for order, i in orders
    a = 1
    b = 2
    
    s1 = step foo
    s2 = step bar

    for x in order
      if x > 0 then s1()
      else s2()

    (ret[[a, b]] or= []).push order
  ret

# very confused, I found "as"(4,3->3,3) modified by later recursive combine invoking(3,2), just because as already in REPL toplevel scope!!!
combine = (m, n) ->
  if n is 1
    xs = ((0 for [1..m]) for [1..m])
    xs[i][i] = 1 for i in [0..m-1]
    return xs
  else if m is n
    return [1 for [1..m]]
  as = combine m - 1, n
  x.push 0 for x in as
  bs = combine m - 1, n - 1
  x.push 1 for x in bs
  #(a[..] for a in as).concat bs
  as.concat bs
