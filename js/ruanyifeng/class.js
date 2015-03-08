class A {
}

class B extends A {
}


class C extends Object {
}

var a = new A();
var b = new B();

console.log(A.prototype, A.__proto__);
console.log(B.__proto__ === A);
console.log(C.__proto__ === Object);
// false
console.log(b.__proto__.__proto__ === a.__proto__)
// true
console.log(b.__proto__);
console.log(b.__proto__.__proto__);
