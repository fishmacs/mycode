promisify = (fn, ctx) ->
  return () ->
    slice = [].slice
    args = slice.call arguments, 0, fn.length - 1
    new Promise (resolve, reject) ->
      args.push (error, result) ->
        if error? reject error
        else resolve result
      fn.apply ctx, args

list = (promises) ->
  new Promise (resolve, reject) ->
    results = []
    done = 0
    promises.forEach (promise, i) ->
      promise.then (result) ->
        results[i] = result
        resolve results if ++done == promises.length
      ,
        reject
      resolve results if promises.length is 0

fs = require 'fs'
fsStat = promisify fs.stat
files = ['/Users/zw/abc1.txt', '/Users/zw/dbdump', '/Users/zw/dump.rdb']
Promise.all(files.map fsStat).then (results) ->
  results.forEach console.log

# seems can not inherited from Promise

class LazyPromise extends Promise
  constructor: (@factory) -> @started = false

  then: ->
    unless @started
      @started = true
      @factory (error, result) ->
        if error then Promise.reject error
        else Promise.resolve result
    super

delayed = new LazyPromise (callback) ->
  console.log 'Started'
  setTimeout ->
    console.log 'Done'
    callback null, 42
  ,
    1000
    
class Module extends LazyPromise
  constructor: (name, deps, factory) ->
    @factory = (callback) =>
      Promise.all(deps).then (apis) =>
        console.log "-- module LOAD: #{name}"
        setTimeOut =>
          console.log "--module done: #{name}"
          api = factory.apply @, apis
          callback null, api
        ,
          1000

A = new Module 'A', [], ->
  logBase: (x, y) ->
    Math.log x / Math.log y
    
B = new Module 'B', [A], (a) ->
  doMath: (x, y) ->
    "B result is: #{a.logBase x, y}"

C = new Module 'C', [A], (a) ->
  doMath: (x, y) ->
    "C result is: #{a.logBase x, y}"
  
D = new Module 'D', [B, C], (b, c) ->
  run: (x, y) ->
    console.log b.doMath(x, y)
    console.log c.doMath(x, y)
