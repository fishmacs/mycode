EventEmitter = require('events').EventEmitter
domain = require 'domain'

d1 = domain.create()
d2 = domain.create()

d1.on 'error', (err) ->
  console.log 'handled by d1!'

d2.on 'error', (err) ->
  console.log 'handled by d2!'
  
# Enter the first domain
d1.run ->
  # this emitter is implicitly bound to d1
  implicitEmitter = new EventEmitter()
  # implicitEmitter.on 'error', ->
  #   console.log process.domain is d1 # true
  implicitEmitter.emit 'error', new Error('for d1')

  # Explicitly bind this emitter to d2
  explicitEmitter = new EventEmitter()
  d2.add explicitEmitter

  # explicitEmitter.on 'error', ->
  #   console.log process.domain is d2 # true
  explicitEmitter.emit 'error', new Error 'for d2'
  
