/**
 * Return an array with the specified value in or not in the array
 * TODO Maybe not the cleanest solution, but this should work for now
 * @param {*} array The array to operate on
 * @param {*} value The value to toggle in the array
 * @param {*} is_set Whether the value should be in the array
 * @returns {array} A new array with the value set as specified
 */
export const getArrayToggleValue = (array, value, is_set) => {
    if (is_set && !array.includes(value)) {
        return array.concat(value)
    } else if (!is_set && array.includes(value)) {
        return array.filter(x => x !== value);
    }
    return array
}