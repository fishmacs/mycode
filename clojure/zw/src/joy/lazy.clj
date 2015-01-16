(def very-lazy (-> (iterate #(do (print \.) (inc %)) 1) rest rest rest))

(def less-lazy (-> (iterate #(do (print \.) (inc %)) 1) next next next))

(defn rec-step [[x & xs]]
  (if x
    [x (rec-step xs)]
    []))

(defn lz-rec-step [s]
  (lazy-seq
   (if (seq s)
     [(first s) (lz-rec-step (rest s))]
     [])))

(defn triangle [n]
  (/ (* n (+ n 1)) 2))

(def tri-nums (map triangle (iterate inc 1)))

(defn nom [n]
  (take n (repeatedly #(rand-int n))))

(defn sort-parts [work]
  (lazy-seq
   (loop [[part & parts] work]
     (println work)
     (if-let [[pivot & xs] (seq part)]
       (let [smaller? #(< % pivot)]
         (recur (list*
                 (filter smaller? xs)
                 pivot
                 (remove smaller? xs)
                 parts)))
       (when-let [[x & parts] parts]
         (cons x (sort-parts parts)))))))

(defn qsort [xs]
  (sort-parts (list xs)))
