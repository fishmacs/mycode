EventEmitter = require('events').EventEmitter

class Test extends EventEmitter
  constructor: ->
    super
    
  test: ->
    @emit 'error', new Error 'test'
    yield return
    
class Tester
  constructor: ->
    @t = new Test
    @t.on 'error', (err) ->
      console.log 'get error in on......'
      
  test: ->
    try
      yield @t.test()
    catch e
      console.log 'get error in catch......'

describe 'Testing error processing', ->
  t = new Tester

  it 'The err should be got in catch, until comment "@t.on..." in Tester constructor', ->
    yield t.test()

