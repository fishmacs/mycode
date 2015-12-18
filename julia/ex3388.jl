using Match

const operators = [+, -, *, /] #"+-*/"
const opCombine = vec([[o1, o2, o3] for o1 in operators, o2 in operators, o3 in operators])

getOperands() =
  map(item -> [(in(i, item) ? 3 : 8) for i in [1:4;]],
      combinations([1:4;], 2))

abstract Tree

#type EmptyT

type Leaf <: Tree
  val:: Rational{Int64}
end

type EvalNode <: Tree
  operator:: Function
  left:: Tree
  right:: Tree
end

evalTree(tree) = @match tree begin
  Leaf(val) => val
  EvalNode(op, left, right) => op(evalTree(left), evalTree(right))
end

addTree(op, d, tree) = @match tree begin
  Leaf(val) => [EvalNode(op, Leaf(d), tree)]
  EvalNode(op1, left, right) => begin
    newtree = [EvalNode(op1, subtree, right) for subtree in addTree(op, d, left)]
    unshift!(newtree, EvalNode(op, Leaf(d), tree))
  end
end

buildTree(operators, operands) = @match (operators, operands) begin
  ([op], [d1, d2]) => [EvalNode(op, Leaf(d1), Leaf(d2))]
  ([op, ops...], [d, ds...]) => begin
    result = []
    for tree in buildTree(ops, ds)
      append!(result, [newtree for newtree in addTree(op, d, tree)])
    end
    result
  end
end

evalTree(tree) = @match tree begin
  Leaf(val) => val
  EvalNode(op, left, right) => begin
    l = evalTree(left)
    r = evalTree(right)
    if (op == /) && r == 0
      0
    else
      op(l, r)
    end
  end
end

function resolve()
  for ops in opCombine
    for ds in getOperands()
      for tree in buildTree(ops, ds)
        if evalTree(tree) == 24
          println(tree)
        end
      end
    end
  end
end
