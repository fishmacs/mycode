lend3 amount balance
  | amount <= 0 = Nothing
  | amount > reserve * 0.5 = Nothing
  | otherwise = Just newBalance
  where reserve = 100
        newBalance = balance - amount
