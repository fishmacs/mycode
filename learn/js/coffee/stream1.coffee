offset = 0
process.stdin.on 'readable', ->
  buf = process.stdin.read()
  return if not buf
  while offset < buf.length
    if buf[offset] is 10
      console.dir buf[0..offset-1].toString()
      buf = buf[offset+1..]
      offset = 0
      process.stdin.unshift buf
      return
    offset++
  process.stdin.unshift buf
