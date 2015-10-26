test = ->
  y = 10
  y++
  ++y
  console.log y or x

test()
  
greet = (name) ->
  for time in ['morning', 'afternoon', 'night']
    console.log "Good #{time}, #{name}"
