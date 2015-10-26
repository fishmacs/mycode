chai = require('chai').should()
chai.use reuqire 'chai-jquery'
  
describe 'Guest list test', ->
  $list = $ '#guestlist-view'
  checkedinClass = 'icon-check'
  guestSelector = '.guest'

  it 'List elmements should have guest.', ->
    $list.length.should.be.ok

  describe 'Click guest test', ->
    $guest = $($list.find(guestSelector)[0])
    guestExists = !!$guest[0]

    $guest.click()
    it 'Should be checked on click', ->
      $guest.should.have.class checkedinClass

    $guest.click()
    it 'Should toggle off when clicked again', ->
      guestExists.should.be.true
      $guest.should.not.have.class checkedinClass
      
  
