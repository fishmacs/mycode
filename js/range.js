'use strict';

function range(begin, end) {
  if (end === undefined) {
    end = begin;
    begin = 0;
  }
  return Array.from(new Array(end).keys()).slice(begin);
}
