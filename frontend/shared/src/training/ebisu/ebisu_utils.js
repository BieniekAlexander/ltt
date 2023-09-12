const ebisu = require('ebisu-js');
import { Recall } from '../recall'

// TODO somehow I found that interval was set to some crazy high number, >1e5
// not sure how that happened, but it was maybe related to me manually setting interval to -1 in the database
// for testing, maybe that made math weird? figure out how that happened, make sure it doesn't happen

/**
 * Recalculate the memory stats of a term
 * @param {object} stats
 * @param {symbol} recall
 */
export function stats_update(stats, recall) {
    // this code would probably be a lot cleaner in TS
    // TODO this code currently fails when score is not equal to 0 or 1, which is a limitation of ebisu
    //      using this temporary hack - it seems that updateRecall(..., num/denom, 1, ...) is approx updateRecall(..., num, denom, ...)
    // another interesting tidbit - it seems that multiple updates in the same session, where time since last study is the same,
    //      evaluates to approximately the same value as one big update
    let score_frac = [Recall.toValue(recall), Recall.toValue(Recall.EASY)]

    if (recall == Recall.FORGET) {
        throw new Error("forgetting should not be handled here, it should be handled at the study entry level!")
    } else if (recall == Recall.SUSPEND) {
        stats.suspended = true
    } else {
        let new_prior = ebisu.updateRecall(
            [stats.alpha, stats.beta, stats.half_life],
            score_frac[0], score_frac[1], Date.now()/1000 - stats.last_study_time)
     
        stats.alpha = new_prior[0]
        stats.beta = new_prior[1]
        stats.half_life = new_prior[2]
    }
}

/**
 * Puts the study entry back into the queue if the interval is in the future
 * @param {list} studyQueue
 * @param {object} entry
 */
export function push_study_entry(studyQueue, entry, recall) {
    let score = Recall.toValue(recall)/Recall.toValue(Recall.EASY)
    // TODO - aggregate the score of the term for the study session

    if (
        (score <= .5)
        && ([Recall.UNKNOWN, Recall.BAD, Recall.GOOD, Recall.EASY].includes(recall))
    ) {
        studyQueue.push(entry)
    }
}