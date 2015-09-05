# 普通的memoize只对显示调用有效，无法对递归中的函数调用使用memoize
memoizer = (memo, fundamental) ->
  shell = (n) ->
    result = memo[n]
    unless typeof result is 'number'
      result = fundamental shell, n
      memo[n] = result
    result

fibonacci = memoizer [0, 1], (shell, n) -> shell(n-1) + shell(n-2)
