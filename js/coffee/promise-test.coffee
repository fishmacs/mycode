promisify = require './promisify'

func = (callback) ->
  callback null, 1

pf = promisify func
