(ns rogue.core
  ;; (:use [caves.ui.core :only [->UI]]
  ;;       [caves.ui.drawing :only [draw-game]]
  ;;       [caves.entities.core :only [tick]]
  ;;       [caves.ui.input :only [get-input process-input]])
  (:require [lanterna.screen :as s]))


; Data Structures ----------------------------
(defrecord Game [world uis input debug-flags])

; Main ---------------------------------------
;; (defn tick-entity [world entity]
;;   (tick entity world))

;; (defn tick-all [world]
;;   (reduce tick-entity world (vals (:entities world))))

(defn clear-messages [game]
  (assoc-in game [:world :entities :player :messages] nil))

;; (defn run-game [game screen]
;;   (loop [{:keys [input uis] :as game} game]
;;     (when (seq uis)
;;       (recur (if input
;;                (-> game
;;                    (dissoc :input)
;;                    (process-input input))
;;                (-> game
;;                    (update-in [:world] tick-all)
;;                    (draw-game screen)
;;                    (clear-messages)
;;                    (get-input screen)))))))

;; (defn new-game []
;;   (map->Game {:world nil
;;               :uis [(->UI :start)]
;;               :input nil
;;               :debug-flags {:show-regions false}}))

;; (defn main
;;   ([] (main :swing false))
;;   ([screen-type] (main screen-type false))
;;   ([screen-type block?]
;;      (letfn [(go []
;;                  (let [screen (s/get-screen screen-type)]
;;                    (s/in-screen screen
;;                                 (run-game (new-game) screen))))]
;;        (if block?
;;          (go)
;;          (future go)))))

(defn main [screen-type]
  (let [screen (s/get-screen screen-type)]
    (s/in-screen screen
                 (s/put-string screen 0 0 "Welcome to the Caves of Clojure!")
                 (s/put-string screen 0 1 "Press any key to exit...")
                 (s/redraw screen)
                 (s/get-key-blocking screen))))

(defn -main [& args]
  (let [args (set args)
        screen-type (cond
                     (args ":swing") :swing
                     (args ":text") :text
                     :else :auto)]
    (main screen-type)))

(comment
  (main :swing false)
  (main :swing true))
