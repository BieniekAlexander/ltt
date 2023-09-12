export class Recall { // TODO maybe change this stuff to type script? https://www.freecodecamp.org/news/how-to-add-typescript-to-a-javascript-project/
    static FORGET = Symbol("FORGET")
    static SUSPEND = Symbol("SUSPEND")
    static UNKNOWN = Symbol("UNKNOWN")
    static BAD = Symbol("BAD")
    static GOOD = Symbol("GOOD")
    static EASY = Symbol("EASY")

    static enumMap = {
        "-2": Recall.FORGET,
        "-1": Recall.SUSPEND,
        "0": Recall.UNKNOWN,
        "1": Recall.BAD,
        "2": Recall.GOOD,
        "3": Recall.EASY
    }

    static valueMap = Object.fromEntries(
        Object
            .entries(Recall.enumMap)
            .map(([key, value]) => [value, key])
    )

    static fromValue(value) {
        return Recall.enumMap[value]
    }

    static toValue(symbol) {
        return parseInt(Recall.valueMap[symbol])
    }
}