module.exports = (fn, ctx) ->
  return () ->
    slice = Array.prototype.slice
    args = slice.call arguments, 0, fn.length - 1
    new Promise (resolve, reject) ->
      args.push () ->
        result = slice.call arguments
        error = result.shift()
        result = result[0] if result.length < 2

        if error? reject error
        else resolve result
      fn.apply ctx, args
