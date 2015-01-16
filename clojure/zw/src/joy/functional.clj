(defn mk-cps [accept? end-value kend kont]
  (fn [n]
    ((fn [n k]
       (let [cont (fn [v] (k (kont v n)))]
         (if (accept? n)
           (k end-value)
           (recur (dec n) cont))))
     n kend)))

(def fac (mk-cps zero? 1 identity #(* % 1 %2)))

(def fac (mk-cps zero? 1 identity *))
