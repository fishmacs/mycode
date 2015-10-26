EventEmitter = require('events').EventEmitter
domain = require 'domain'

emitter = new EventEmitter
d1 = domain.create()
d1.on 'error', (err) ->
  console.log 'Handled by domain: ', err.stack
d1.add emitter

emitter.on 'error', (err) ->
  console.log 'Handled by listener: ', err.stack
emitter.emit 'error', new Error 'This will be handled by listener'

emitter.removeAllListeners 'error'
emitter.emit 'error', new Error 'This will be handled by domain'

d1.remove emitter
emitter.emit 'error', new Error 'woops, unhandled error. This is converted to an exception. Time to crash!'
  
