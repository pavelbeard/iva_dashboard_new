Object.defineProperty(String.prototype, 'capitalize', {
    value: function () {
        return this.charAt(0).toUpperCase() + this.slice(1);
    },
    enumerable: false
})

Object.defineProperty(String.prototype, 'toCamelCase', {
    value: function () {
        let t = [];
        this.split(/[\s_,.;:|/]/).forEach((str, i=0) =>{
            if (i !== 0) {
                t.push(str.charAt(0).toUpperCase() + str.slice(1));
                i++;
            }
            else t.push(str)
        });
        return "".concat(t).replace(/,/g, '');
    },
    enumerable: false
});

Object.defineProperty(String.prototype, 'toCapitalizePythonKey', {
    value: function () {
        let t = [];
        this.split(/[\s_,.;:|/]/).forEach((str, i=0) =>{
             if (i === 0) t.push(str.charAt(0).toUpperCase() + str.slice(1));
             else t.push(str);
        });
        return "".concat(t).replace(/,/g, ' ');
    },
    enumerable: false
})

Object.defineProperty(String.prototype, 'safeParseInt', {
    value: function () {
        try {
            let t = parseInt(this)
            return t;
        } catch (e) {
            return this
        }
    },
    enumerable: false
})

// Object.defineProperty(Object.prototype, 'mapObject', {
//     value: function (object) {
//         return this.args;
//     },
//     enumerable: true
// })

/**
 * Метод, добавляющий всплывающую информацию об опрошенных частях сервера.
 * @param targetElem html-элемент карточки целевого хоста.
 * @param htmlMarkup html разметка.
 * @param cardPart часть сервера.
 */
export function dropdownTitle(targetElem, htmlMarkup, cardPart) {
    $(function () {
         targetElem.find(cardPart).hover(function () {
             if (targetElem.attr('data-available') !== "false") {
                 $(this).addClass('show');
                 $(this).find('.dropdown-menu').addClass('show');
                 $(this).find('.dropdown-menu').html(htmlMarkup);
             }
         }, function () {
             $(this).removeClass('show');
             $(this).find('.dropdown-menu').removeClass('show');
             $(this).find('.dropdown-menu').empty()
         });
    });
}

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
