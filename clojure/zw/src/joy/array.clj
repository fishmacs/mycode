(doto (StringBuilder. "abc")
  (.append (into-array Character/TYPE [\x \y \z])))
