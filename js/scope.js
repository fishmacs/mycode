'use strict';

const MAX_VALUE = 4;

const counter = function (max=MAX_VALUE) {
  let i = 0;
  let s = `a${i}bc`;
  for(let i = 1; i <= max; i++)
    console.log(i);
  console.log(i);
};

counter();
