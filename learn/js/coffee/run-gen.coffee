runGenObj = (genObj, callbacks=undefined) ->
  handleOneNext()
  
  handleOneNext = (prevResult=null) ->
    try
      yielded = genObj.next prevResult
      if yielded.done
        callbacks.success yielded.value unless yielded.value is undefined
      else
        setTimeout runYieldedValue, 0, yielded.value
    catch error
      if callbacks then callbacks.failure(error)
      else throw error

  runYieldedValue = (yieldedValue) ->
    if yieldedValue is undefined
      handleOneNext callbacks
    else if Array.isArray yieldedValue
      runInParallel yieldedValue
    else
      runGenObj yieldedValue,
        success: (result) -> handleOneNext result,
        failure: (err) -> genObj.throw err

  runInParallel = (genObjs) ->
    resultArray = new Array genObjs.length
    resultCountdown = genObjs.length
    for genObj, i in genObjs
      runGenObj genObj
        success: (result) ->
          resultArray[i] = result
          if --resultCountdown <= 0
            handleOneNext resultArray
        failure: (err) ->
          genObj.throw err
  
run = (genFunc) -> runGenObj genFunc()
