String.prototype.allReplace = function (obj){
    let retStr = this;
    for (let x in obj) {
        retStr = retStr.replace(new RegExp(x, 'g'), obj[x]);
    }
    return retStr;
};

// export function zip(...arr) {
//     return Array(Math.max(...arr.map(a => a.length)))
//         .fill()
//         .map((_, i) => arr.map(a => a[i]))
// }
//
// const a = [1, 2, 3];
// const b = ["a", "b", "c"];

/**
 * Zips any number of iterables. It will always zip() the largest Iterable returning undefined for shorter arrays.
 * @param  {...Iterable<any>} iterables
 */
function* zip(...iterables) {
  // get the iterator of for each iterables
  const iters = [...iterables].map((iterable) => iterable[Symbol.iterator]());
  let next = iters.map((iter) => iter.next().value);
  // as long as any of the iterables returns something, yield a value (zip longest)
  while(anyOf(next)) {
    yield next;
    next = iters.map((iter) => iter.next().value);
  }

  function anyOf(arr){
    return arr.some(v => v !== undefined);
  }
}

export {zip};