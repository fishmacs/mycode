(defmacro do-until [& clauses]
  (when clauses
    (list `when (first clauses)
          (if (next clauses)
            (second clauses)
            (throw (IllegalArgumentException.
                    "do-until requires an even number of forms")))
          (cons 'do-until (nnext clauses)))))

(defmacro unless [condition & body]
  `(if (not ~condition)
     (do ~@body)))

(defmacro def-watched [name & value]
  `(do
     (def ~name ~@value)
     (add-watch (var ~name)
                :re-bind
                (fn [~'key ~'r old# new#]
                  (println old# " -> " new#)))))

(defmacro domain [name & body]
  `{:tag :domain
    :attrs {:name (str '~name)}
    :content [~@body]})

(declare handle-things)

(defmacro grouping [name & body]
  `{:tag :grouping
    :attrs {:name (str '~name)}
    :content [~@(handle-things body)]})

(declare grok-attrs grok-props)

(defn handle-things [things]
  (for [t things]
    {:tag :thing
     :attrs (grok-attrs (take-while (comp not vector?) t))
     :content (if-let [c (grok-props (drop-while (comp not vector?) t))]
                [c]
                [])}))

(defn grok-attrs [attrs]
  (into {:name (str (first attrs))}
        (for [a (rest attrs)]
          (cond
           (list? a) [:isa (str (second a))]
           (string? a) [:comment a]))))

(defn grok-props [props]
  (when props
    {:tag :properties
     :attrs nil
     :content (apply vector
                     (for [p props]
                       {:tag :property
                        :attrs {:name (str (first p))}
                        :content nil}))}))

(def d
  (domain man-vs-monster
    (grouping people
      (Human "A stock human")
      (Man (isa Human)
           "A man, baby"
           [name]
           [has-beard?]))
    (grouping monsters
      (Chupacabra
       "A fierce, yet elusive creature"
       [eats-goats?]))))

(defmacro awhen [expr & body]
  `(let [~'it ~expr]
     (when ~'it
       (do ~@body))))

(import [java.io BufferedReader InputStreamReader]
        [java.net URL])

(defn joc-www [url]
  (-> url URL. .openStream InputStreamReader. BufferedReader.))

(let [stream (joc-www "http://www.baidu.com")]
  (with-open [page stream]
    (println (.readLine page))
    (print "The stream will now close... "))
  (println "but let's read from it anyway.")
  (.readLine stream))

(defmacro with-resource [binding close-fn & body]
  `(let ~binding
     (try
       (do ~@body)
       (finally
         (~close-fn ~(binding 0))))))

(let [stream (joc-www "http://www.baidu.com")]
  (with-resource [page stream]
    #(.close %)
    (.readLine page)))
