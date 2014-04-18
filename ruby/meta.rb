class Hash
  def method_missing(key, *args)
    text = key.to_s
    if text[-1, 1] == '='
      self[text.chop.to_sym] = args[0]
    else
      self[key]
    end
  end
end
