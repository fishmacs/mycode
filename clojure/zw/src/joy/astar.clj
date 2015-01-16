(def world [[  1   1   1   1   1]
            [999 999 999 999   1]
            [  1   1   1   1   1]
            [  1 999 999 999 999]
            [  1   1   1   1   1]])

(defn neighbors
  ([size yx] (neighbors [[-1 0] [1 0] [0 -1] [0 1]] size yx))
  ([deltas size yx]
     (filter (fn [new-yx]
               (every? #(< -1 % size) new-yx))
             (map #(vec (map + yx %)) deltas))))

(defn estimate-cost [step-cost-est size y x]
  (* step-cost-est
     (- (+ size size) y x 2)))

(defn path-cost [node-cost cheapest-nbr]
  (+ node-cost (:cost cheapest-nbr 0)))

(defn total-cost [newcost step-cost-est size y x]
  (+ newcost
     (estimate-cost step-cost-est size y x)))

(defn min-by [f coll]
  (when (seq coll)
    (reduce (fn [min this]
              (if (> (f min) (f this)) this min))
            coll)))

(defn astar [start-yx step-est cell-costs]
  (let [size (count cell-costs)]
    (loop [steps 0
           routes (vec (replicate size (vec (replicate size nil))))
           work-todo (sorted-set [0 start-yx])]
      (if (empty? work-todo)
        [(peek (peek routes)) :steps steps]
        (let [[_ yx :as work-item] (first work-todo)
              rest-work-todo (disj work-todo work-item)
              nbr-yxs (neighbors size yx)
              cheapest-nbr (min-by :cost
                                   (keep #(get-in routes %) nbr-yxs))
              newcost (path-cost (get-in cell-costs yx)
                                 cheapest-nbr)
              oldcost (:cost (get-in routes yx))]
          ;; (println work-todo)
          ;; (println routes)
          ;; (println cheapest-nbr)
          ;; (println yx newcost oldcost)
          (if (and oldcost (>= newcost oldcost))
            (recur (inc steps) routes rest-work-todo)
            (recur (inc steps)
                   (assoc-in routes yx
                             {:cost newcost
                              :yxs (conj (:yxs cheapest-nbr [])
                                         yx)})
                   (into rest-work-todo
                         (map
                          (fn [w]
                            (let [[y x] w]
                              [(total-cost newcost step-est size y x) w]))
                          nbr-yxs)))))))))

(defn estimate-cost1 [step-cost-est start-yx end-yx]
  (let [[y0 x0] start-yx
        [y1 x1] end-yx]
    (* step-cost-est
       (+ (- y1 y0) (- x1 x0)))))

(def min-map[f coll]
    (reduct-kv #((if (> (f %3))))
      ))
(defn process-points [yxs open-table close-table]
  (let [yx (first yxs)]
    (if yx
      (if (close-table yx)
        (recur (rest yxs) open-table close-table)
        if (open-table)
        )
      
      ))
(defn astar1 [start-yx end-yx step-est cell-costs]
  (let [size (count cell-costs)
        [y x] start-yx
        [h0 (estimate-cost1 step-est start-yx end-yx)]
        [g0 (get-in cell-costs start-yx)]
    (loop [steps 0
           yx start-yx
           open-table {start-yx {:h h0 :g g0 :f (+ g0 h0)}}
           close-table {}]
      (if (close-table end-yx)
        {:route (get-route close-table end-yx)
         :cost ((get-in close_table end-yx) :f)
         :steps steps}
        (let [cheapest-nbr (min-by :f open-table)
              nbr-yxs (neighbors size yx)
              [nex-yx, new-open, new-close] (process-points nbr-yxs)]
          
