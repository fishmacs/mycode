EventEmitter = require('events').EventEmitter
domain = require 'domain'

d1 = domain.create()
d2 = domain.create()

# Enter the first domain
d1.run ->
  # this emitter is implicitly bound to d1
  implicitEmitter = new EventEmitter()
  implicitEmitter.on 'someEvent', ->
    console.log process.domain is d1 # true
  implicitEmitter.emit 'someEvent'

  # Explicitly bind this emitter to d2
  explicitEmitter = new EventEmitter()
  d2.add explicitEmitter

  explicitEmitter.on 'someEvent', ->
    console.log process.domain is d2 # true
  explicitEmitter.emit 'someEvent'
  
