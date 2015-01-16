(defmacro anarithmetic [& exprs]
  (reduce (fn [rest expr]
            `(let ~['it expr]
               ;; (println "it" ~'it)
               ;; (println "rest" ~rest)
               ~rest))
          'it
          (reverse exprs)))
