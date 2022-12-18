// TODO do BFF pattern insteasd of duplicating algorithm

const STEP_INTERVALS = [0, 1, 3, 10]

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

/**
 * Recalculate the memory stats of a term
 * @param {object} stats
 * @param {int} recall
 */
export function stats_update(stats, recall) {
    stats.recall = recall

        if (stats.step == -1) { // in review phase
            if (recall == 0) {
                stats.step = 0
                stats.ef *= Math.max(RECALL_EASINESS_FACTORS[recall], 1.3)
            } else if (recall == 1) {
                stats.ef *= Math.max(RECALL_EASINESS_FACTORS[recall], 1.3)
                stats.interval *= RECALL_INTERVALS[recall]
             } else {
                stats.ef *= Math.max(RECALL_EASINESS_FACTORS[recall], 1.3)
                stats.interval *= stats.ef
            }
        } else { // in learning phase
            if (recall == 0) {
                stats.step = 0
            } else if (recall == 2) {
                stats.step = stats.step+1==STEP_INTERVALS.length ? -1 : stats.step+1
            } else if (recall == 3) {
                stats.step = -1
            }

            if (stats.step != -1) {
                stats.interval = STEP_INTERVALS[stats.step]
            }
        }
}

/**
 * Initialize the Stats object for the training session
 * @param {object} stats
 */
export function stats_session_init(stats) {
    stats.recall = null
}

/**
 *  Update the stats of the object after it's been studied
 * @param {object} stats
 */
export function session_update(stats) {
    // pass - doesn't do anything
}

/**
 * Puts the study entry back into the queue if the interval is in the future
 * @param {list} studyQueue
 * @param {object} entry
 */
export function push_study_entry(studyQueue, entry) {
    let step = entry.stats.definition.step
    let interval = STEP_INTERVALS[step]

    if (interval == 0) {
        // less than Recall.GREAT
        studyQueue.push(entry)
    }
}