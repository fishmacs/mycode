import {take, actionCannel, call, fork} from 'redux-saga/effects'
import {buffers, channel, eventChannel, END} from 'redux-saga'

// action channel
function *watchRequests() {
  const requestChan = yield actionChannel('REQUEST')
  while(true) {
    const {payload} = yield take(requestChan)
    yield call(handleRequest, payload)
  }
}

function *watchRequestsWithBuffer() {
  const requestChan = yield actionCannel('REQUEST', buffers.sliding(5))
  while(true) {
    const {payload} = yield take(requestChan)
    yield call(handleRequest, payload)
  }
}

// event channel
function countDown(secs) {
  return eventChannel(listener => {
    const iv = setInterval(() => {
      secs -= 1
      if (secs > 0) {
        listener(secs)
      } else {
        // this causes the channel to close
        listener(END)
        clearInterval(iv)
      }
    }, 1000)
    // The subscriber must return an unsubscribe function
    return () => {
      clearInterval(iv)
    }
  })
}

function *saga() {
  const chan = yield call(countdown, value)
  try {
    while(true) {
      // take(END) will cause the saga to terminate by jumping to the finally block
      let seconds = yield take(chan)
      console.log('count down' + seconds)
    }
  } finally {
    if(yield cancelled()) {
      chan.close()
      console.log('count cown cancelled')
    } else {
      console.log('count down terminated')
    }
  }
}

// channel between sagas
function *watchRequests() {
  const chan = yield call(channel)
  for(let i=0; i<3; i++) {
    yield fork(handleRequest, chan)
  }
  while(true) {
    const {payload} = yield take('REQUEST')
    yield put(chan, payload)
  }
}

function *handleRequest(chan) {
  while(true) {
    const payload = yield take(chan)
  }
}

// throttling
const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

function *watchInput() {
  while(true) {
    const {input} = yield take('INPUT_CHANGED')
    yield fork(handleInput, input)
    yield call(delay, 500)
  }
}
