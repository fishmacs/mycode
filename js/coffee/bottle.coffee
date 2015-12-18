price = 2
bottles = 2
caps = 4

bottleToBeer = (n) ->
  [Math.floor(n / bottles), n % bottles]

capToBeer = (n) ->
  [Math.floor(n / caps), n % caps]

drink = (n) ->
  beerNum = Math.floor n / price
  bottleNum = capNum = beerNum
  while capNum or bottleNum
    [beer1, remainBottle] = bottleToBeer bottleNum
    [beer2, remainCap] = capToBeer capNum

    beer = beer1 + beer2
    break if not beer

    bottleNum = remainBottle + beer
    capNum = remainCap + beer
    beerNum += beer
    console.log beerNum, bottleNum, capNum
  console.log beerNum, bottleNum, capNum
