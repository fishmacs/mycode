p1 = new Promise (resolve, reject) ->
  setTimeout (-> resolve 1), 5

p2 = Promise.resolve 2

p1.then console.log.bind console
p2.then console.log.bind console

