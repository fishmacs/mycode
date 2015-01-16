(ns joy.gui.DynaFrame
  (:gen-class
   :name       joy.gui.DynaFrame
   :extends    java.swing.JFrame
   :implements [clojure.lang.IMeta]
   :prefix     df-
   :state      state
   :init       init
   :constructors {[String] [String]}
   :methods [[display [java.awt.Container] void]
             ^{:static true} [version [] String]])
  (:import (javax.swing JFrame JPanel)
           (java.awt BorderLayout Container)))
