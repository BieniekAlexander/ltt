/**
 * Functions of the Supermemory 2 algorithm
 *
 * source: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
*/
// TODO do BFF pattern insteasd of duplicating algorithm

/**
 * Recalculate the easiness factor
 *  @param {float} ef
 * @param {int} recall 
 * @return {float} the easiness factor
 */
function get_easiness_factor(ef, recall) {
    let q = recall
    return max(ef - .8 + .28 * q - .02 * q ** 2, 1.3)
}

/**
 * calculate the next repetition interval
 *  @param {int} ef
 * @param {float} repetition 
 * @return {int} the number of sessions until next review
 */
function get_repetition_interval(repetition, ef) {
    let interval = 0

    if (repetition == 1) {
        return 1
    } else if (repetition == 2) {
        interval = 6
    } else {
        interval = get_repetition_interval(repetition - 1, ef) * ef
    }

    return Math.ceil(interval)
}

/**
 * Recalculate the repetition count we're on
 * @param {int} repetition
 * @param {float} recall 
 * @return {int} the repetition count
 */
function get_repetition(repetition, recall) {
    if (recall > 2) {
        return repetition + 1
    } else {
        return 1
    }
}

/**
 * Recalculate the memory stats of a term
 * @param {object} stats
 * @param {int} recall
 */
function stats_update(stats, recall) {
    stats.ef = get_easiness_factor(stats.ef, recall)
}

/**
 * Initialize the Stats object for the training session
 * @param {object} stats
 */
function stats_init(stats) {
    stats.ef = 2.5
    stats.recall = null
}

/**
 *  Update the stats of the object after it's been studied
 * @param {object} stats
 */
function session_update(stats) {
    if (stats.recall != null) {
        statas.repetition = get_repetition(stats.repetition, stats.recall)
        stats.interval = get_repetition_interval(stats.repetition, stats.ef)
    }
}