request = (url) ->
  console.log url
  Promise.resolve url

foo = ->
  yield request 'http://some.url.2'
  yield request 'http://some.url.3'

bar = ->
  yield request 'http://some.url.1'
  yield from foo()

