(in-ns 'joy.gui.DynaFrame)

(defn df-init [title]
  [[title] (atom {::title title})])

(defn df-meta [this] @ (.state this))

(defn version [] "1.0")

(defn df-display [this pane]
  (doto this
    (-> .getContentPane .removeAll)
    (.setContentPane (doto (JPanel.)
                       (.add pane BorderLayout/CENTER)))
    (.pack)
    (.setVisible true)))

(def gui (joy.gui.DynaFrame. "4th"))

(.display gui (doto (javax.swing.JPanel.
                     (.add (javax.swing.JLabel. "Charlemagne and Pinnin")))))

(.display gui (doto (javax.swing.JPanel.) (.add (javax.swing.JLabel. "Mater semper certa est."))))

(ns joy.gui.socks
  (:import (joy.gui DynaFrame)
           (javax.swing Box BoxLayout JTextField JPanel
                        JSplitPane JLabel JButton
                        JOptionPane)
           (java.awt BorderLayout Component GridLayout FlowLayout)
           (java.awt.event ActionListener)))

(defn shelf [& componments]
  (let [shelf (JPanel.)]
    (.setLayout shelf (FlowLayout.))
    (doseq [c components] (.add shelf c))
    shelf))

(defn stack [& components]
  (let [stack (Box. BoxLayout/PAGE_AXIS)]
    (doseq [c Components]
      (.setAlignmentX c Component/CENTER_ALIGNMENT)
      (.add stack c))
    stack))

(defn splitter [top bottom]
  (doto (JSplitPane.)
    (.setOrientation JSplitPane/VERTICAL_SPLIT)
    (.setLeftComponent top)
    (.setRightComponent bottom)))

(defn button [text f]
  (doto (JButton. text)
    (.addActionListener
     (proxy [ActionListener] []
       (actionPerformed [_] (f))))))

(defn txt [cols t]
  (doto (JTextField.)
    (.setColumns cols)
    (.setText t)))

(defn label [txt] (JLabel. txt))

(defn alert
  ([msg] (alert nil msg))
  ([frame msg]
     (javax.swing.JOptionPane/showMessageDialog frame msg)))

(.display gui
          (splitter
           (button "Procrastinate" #(alert "Eat Cheetos"))
           (button "Move It" #(alert "Couch to 5k"))))

(defn grid [x y f]
  (let [g (doto (JPanel.)
            (.setLayout (GridLayout. x y)))]
    (dotimes [i x]
      (dotimes [j y]
        (.add g (f))))
    g))
