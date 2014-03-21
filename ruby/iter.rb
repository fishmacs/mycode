def sequence(n, m, c)
  i, s = 0, []
  while(i < n)
    y = m*i + c
    if block_given?
      s << (yield y)
    else
      s << y
    end
    i += 1
  end
  s
end
