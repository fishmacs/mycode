should = require('chai').should()

post = require '../interface1'

myPost = post.post().set 'message', 'Hello, world!'

describe 'Interface example', ->
  myPost.save()
  storage = JSON.parse post.localStorage.storage
  storedMessage = storage[myPost.id].message

  it '.save() method should save post.', ->
    storedMessage.should.equal 'Hello, world!'
