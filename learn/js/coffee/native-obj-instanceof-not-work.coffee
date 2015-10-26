class A

class B extends A

class MyError extends Error

class Foo
  constructor :-> return foo: 'foo'

class Bar
  ctor = -> foo: 'foo'
  constructor: ctor
