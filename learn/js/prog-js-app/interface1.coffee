stampit = require 'stampit'

generateUUID = ->
  'abcd'
  
localStorage = {}

supportsLocalStorage = localStorage?
storage = null

storageInterface = stampit.methods
  save: -> throw new Error '.save() method not implemented.'

localStorageProvider = stampit
  .compose storageInterface
  .methods save: ->
    localStorage.storage = JSON.stringify storage

cookieProvider = stampit
  .compose storageInterface
  .methods save: ->
    $.cookie 'storage', JSON.stringify storage

post = stampit
  .methods
    save: ->
      storage[@id] = @data
      storage.save()
      @
    set: (name, value) ->
      @data[name] = value
      @
  .state
    data:
      message: '', published: false
    id: undefined
  .enclose ->
    @id = generateUUID()
    @

storage = supportsLocalStorage and localStorageProvider() or cookieProvider()

exports.post = post
exports.localStorage = localStorage


