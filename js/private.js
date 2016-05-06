'use strict';

// keep private data in environment of class ctor
class Countdown {
  constructor(counter, action) {
    Object.assign(this, {
      dec() {
        if (counter < 1) return;
        counter--;
        if (counter === 0) {
          action();
        }
      }
    });
  }
}

// mark private properties via naming convention
class Countdown {
  constructor(couter, action) {
    this._counter = counter;
    this._action = action;
  }

  dec() {
    if (this._counter < 1) return;
    this._counter--;
    if (this._counter === 0) {
      this._action();
    }
  }
}

// keep private data in weak maps
let _counter = new WeakMap();
let _action = new WeakMap();

class Countdown {
  constructor(counter, action) {
    _counter.set(this, counter);
    _action.set(this, action);
  }

  dec() {
    let counter = _counter.get(this);
    if (counter < 1) return;
    _counter.set(this, --counter);
    if (counter === 0) {
      _action.get(this)();
    }
  }
}

// use symbols as keys for private properties
const _counter = Symbol('counter');
const _action = Symbol('action');

class Countdown {
  constructor(counter, action) {
    this[_counter] = counter;
    this[_action] = action;
  }

  dic() {
    if (this[_counter] < 1) return;
    this[_counter]--;
    if (this[_counter] === 0) {
      this[_action]();
    }
  }
}
