OperationFail = (msg) ->
  @message = msg
  @name = 'OperationFail'
  @stack = (new Error).stack
  return
  
OperationFail.prototype = Object.create Error.prototype
OperationFail.prototype.constructor = OperationFail


OperationFail1 = (msg) ->
  @message = msg
  @name = 'OperationFail'
  @stack = (new Error).stack
  return

require('util').inherits OperationFail1, Error
  

class OperationFail2
  constructor: (@message) ->
    @name = @constructor.name

  @:: = new Error()
  @::constructor = @

