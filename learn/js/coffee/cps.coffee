logArray = (arr) ->
  forEachCps arr,
    (elem, index, next) ->
      console.log elem
      next()
    ,
    -> console.log '### Done'

forEachCps = (arr, visitor, done) ->
  forEachCpsRec 0, arr, visitor, done

forEachCpsRec = (index, arr, visitor, done) ->
  if index < arr.length
    visitor arr[index], index,
      -> forEachCpsRec (index+1), arr, visitor, done
  else
    done()

f = -> g (result) -> console.log result
    
g = (success) -> h success

h = (success) -> success 123

searchArray = (arr, searchFor, success, failure) ->
  forEachCps arr,
    (elem, index, next) ->
      if compare elem, searchFor
        success elem
      else
        next()
    ,
    failure

compare = (elem, searchFor) ->
  elem.localeCompare(searchFor) is 0
  
searchArray1 = (arr, searchFor, success, failure) ->
  forEachCps arr,
    (elem, index, next) -> compareCps(elem, searchFor, success, next),
    failure

compareCps = (elem, searchFor, success, next) ->
  if elem.localeCompare(searchFor) is 0
    success elem
  else
    next()

printDiv = (a, b, success, failure) ->
  tryIt (succ, fail) -> # try
    div a, b, (result) ->
      console.log result
      succ()
  ,
  (errorMsg, succ, fail) -> handleError succ, fail
  ,
  success, failure
  
div = (dividend, divisor, success, failure) ->
  if divisor is 0
    throwIt 'Division by zero', success, failure
  else
    success dividend / divisor

tryIt = (tryBlock, catchBlock, success, failure) ->
  tryBlock success, (errorMsg) ->
    catchBlock errorMsg, success, failure

throwIt = (errorMsg, success, failure) ->
  failure errorMsg
