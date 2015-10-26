package ui2

import observer._

trait ObservableClick extends Clickable with Subject {
  abstract override def click() = {
    super.click()
    notifyObservers
  }
}
