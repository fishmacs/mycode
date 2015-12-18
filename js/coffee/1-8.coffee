flat = (arr) ->
  ret = []
  for item in arr
    ret = ret.concat item
  ret

flatMap = (f, arr) ->
  ret = []
  for item in arr
    ret = ret.concat f(item)
  ret

permutate0 = (arr) ->
  if arr.length is 1
    [arr]
  else
    ret = []
    for i in [0..arr.length-1]
      remained = arr[...i].concat arr[i+1..]
      for item in permutate remained
        ret = ret.concat [[arr[i]].concat item]
    ret

intersect = (x, arr) ->
  for i in [0..arr.length]
    a = arr[..]
    a.splice i, 0, x
    a

intersect1 = (x, arr) ->
  if arr.length is 0
    [[x]]
  else
    y = arr[0]
    ys = arr[1..]
    [[x].concat(y, ys)].concat ([y].concat(y1) for y1 in intersect1(x, ys))
    
permutate = (arr) ->
  if arr.length is 0
    [[]]
  else
    flatMap ((item) -> intersect arr[0], item)
    , permutate arr[1..]
    # ret = []
    # for item in permutate arr[1..]
    #   ret = ret.concat intersect(arr[0], item)
    # ret
    ## double "for" is not as same as in Haskell/Python, does not do flat,
    ## in livescript is ok.
    #intersect(arr[0], item) for item in permutate arr[1..]

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

check = ->
  for digits in permutate [1..8]
    if digitsToNum(digits[..2]) * digits[3] is digitsToNum(digits[4..])
      console.log digits
  return

select = (arr) ->
  digits = []
  for i in [0..9]
    digits.push i if arr[i] > 0
  digits

# old version of digitsToNum
group = (arr) ->
  if arr.length is 1
    arr[0]
  else
    group(arr[...-1]) * 10 + arr[arr.length - 1]

digitsToNum = (digits) ->
  digits.reduce ((num, d) -> num * 10 + d), 0
  
check1 = ->
  for item in combine 10, 5
    digits = select item
    for arr in permutate digits
      rds = arr[..].reverse()
      console.log arr if digitsToNum(arr) * 4 is digitsToNum rds
  return


# expriments with comprehension
ops = []
ops.push [o1,o2,o3] for o1 in '+-*/' for o2 in '+-*/' for o3 in '+-*/'

[].concat [[o1,o2,o3]] for o1 in '+-*/' for o2 in '+-*/' for o3 in '+-*/'

[o1,o2,o3] for o1 in '+-*/' for o2 in '+-*/' for o3 in '+-*/'
