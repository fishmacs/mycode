Readable = require('stream').Readable

rs = Readable()
c = 97
rs._read = ->
  rs.push String.fromCharCode c++
  rs.push null if c > 'z'.charCodeAt(0)

rs._read = ->
  if c > 'z'.charCodeAt(0)
    rs.push null
  else
    setTimeout (-> rs.push String.fromCharCode c++), 100
  
rs.pipe(process.stdout)

process.on('exit', -> console.error '\n_read() called ' + (c - 97) + ' times')
process.stdout.on('error', process.exit)
  
