request = (url) ->
  console.log url
  Promise.resolve url

foo = (val) ->
  if val > 1
    val = yield from foo val - 1
  yield request 'http://some.url/?v=' + val

bar = ->
  yield from foo 3

run = (gen, args...) ->
  it = gen.apply @, args
  handleNext = (value) ->
    next = it.next(value)
    handleResult next
  handleResult = (next) ->
    if next.done
      next.value
    else
      Promise.resolve next.value
      .then handleNext, (err) ->
        Promise.resolve it.throw(err)
        .then handleResult
  Promise.resolve()
  .then handleNext
