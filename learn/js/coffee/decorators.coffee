before = (decoration) ->
           (base) ->
             ->
               decoration.apply(this, arguments)
               base.apply(this, arguments)

after = (decoration) ->
           (base) ->
             ->
               __value__ = base.apply(this, arguments)
               decoration.apply(this, arguments)
               __value__

around = (decoration) ->
           (base) ->
             (argv...) ->
               callback = => base.apply(this, argv)
               decoration.apply(this, [callback].concat(argv))

provided = (condition) ->
             (base) ->
               ->
                 if condition.apply(this, arguments)
                   base.apply(this, arguments)
