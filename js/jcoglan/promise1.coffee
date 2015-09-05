util = require 'util'

# seems can not inherited from Promise

LazyPromise1 = (factory) ->
  @factory = factory
  @started = false
  return

util.inherits LazyPromise1, Promise

LazyPromise1.prototype.then = ->
  unless @started
    @started = true
    @factory (error, result) ->
      if error then Promise.reject error
      else Promise.resolve result
  console.log this
  Promise.prototype.then.apply this, arguments

delayed1 = new LazyPromise1 (callback) ->
  console.log 'Started'
  setTimeout ->
    console.log 'Done'
    callback null, 42
  ,
    1000
  
