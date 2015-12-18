const price = 2
const bottles = 2
const caps = 4

bottleToBeer(n) =
  div(n, bottles), n % bottles

capToBeer(n) =
  div(n, caps), n % caps

function drink(n)
  beerNum = div(n, price)
  bottleNum = capNum = beerNum
  while capNum > 0 || bottleNum > 0
    beer1, remainBottle = bottleToBeer(bottleNum)
    beer2, remainCap = capToBeer(capNum)
    beer = beer1 + beer2
    beer > 0 || break
    bottleNum = remainBottle + beer
    capNum = remainCap + beer
    beerNum += beer
  end
  println((beerNum, bottleNum, capNum))
end
  
