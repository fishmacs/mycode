(defn sum-down-from [sum x]
  (if (pos? x)
    (recur (+ sum x) (dec x))
    sum))

(defn sum-down-from0 [x]
  (loop [sum 0, y x ]
    (if (pos? y)
      (recur (+ sum y) (dec y))
      sum)))
