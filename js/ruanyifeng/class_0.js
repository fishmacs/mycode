class A {
}

A.prototype === Function.prototype
// true

class B extends A {
}

B.prototype === C
// true

class C extends Object {
}

C.prototype === Object
// true

var p1 = new Point(2, 3);
var p2 = new ColorPoint(2, 3, 'red');

p2.__proto__ === p1.__proto // false
p2.__proto__.__proto__ === p1.__proto__ // true

