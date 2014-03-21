def fibonacci_generator(x0, y0)
  Fiber.new do
    x, y = x0, y0
    loop do
      Fiber.yield y
      x, y = y, x+y
    end
  end
end
