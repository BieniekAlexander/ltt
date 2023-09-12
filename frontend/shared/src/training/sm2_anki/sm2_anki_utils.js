import { Recall } from '../recall'

const STEP_INTERVALS = [0, 1, 3, 10]
const MAX_INTERVAL = 365

const RECALL_INTERVALS = {
    0: 1,
    1: 1.2
}

const RECALL_EASINESS_FACTORS = {
    0: 0.8,
    1: 0.85,
    2: 1.0,
    3: 1.15
}

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
    stats.recall = Recall.toValue(recall)

    if (recall == Recall.FORGET) {
        throw new Error("forgetting should not be handled here, it should be handled at the study entry level!")
    } else if (recall == Recall.SUSPEND) {
        stats.suspended = true
    } else if (stats.step == -1) { // in review phase
        stats.ef = Math.max(stats.ef*RECALL_EASINESS_FACTORS[Recall.toValue(recall)], 1.3)

        if (recall == Recall.UNKNOWN) {
            stats.step = 0
        } else if (recall == Recall.BAD) {
            stats.interval = Math.floor(stats.interval*RECALL_INTERVALS[Recall.toValue(recall)])
        } else {
            stats.interval = Math.floor(Math.max(stats.ef*stats.interval, 1))
        }
    } else { // in learning phase
        if (recall == Recall.UNKNOWN) {
            stats.step = 0
        } else if (recall == Recall.GOOD) {
            if (stats.step + 1 == STEP_INTERVALS.length) {
                stats.step = -1
                stats.interval = 1
            } else {
                stats.step += 1
            }
        } else if (recall == Recall.EASY) {
            stats.step = -1
            stats.interval = 4
        }

        if (stats.step != -1) {
            stats.interval = STEP_INTERVALS[stats.step]
        }
    }

    // cap the interval to avoid intervals that are too long
    stats.interval = Math.max(stats.interval, MAX_INTERVAL)
}

/**
 * Initialize the Stats object for the training session
 * @param {object} stats
 */
export function stats_session_init(stats) {
    stats.recall = null
}

/**
 * Puts the study entry back into the queue if the interval is in the future
 * @param {list} studyQueue
 * @param {object} entry
 */
export function push_study_entry(studyQueue, fact, entry) {
    let step = entry.stats[fact].step
    let interval = STEP_INTERVALS[step]

    if (interval == 0) {
        // less than Recall.GREAT
        studyQueue.push(entry)
    }
}