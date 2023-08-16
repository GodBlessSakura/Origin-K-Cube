function graph_traversal(triples, activities, courseCode) {
    let firstHop =
        triples.filter(triple => triple.h_name == courseCode || triple.t_name == courseCode)
        .map(triple => {
            let theOther = [triple.h_name, triple.t_name].filter(e => e != courseCode)[0]
            return theOther
        })
    let newData = {}
    let oldData = {}
    oldData[courseCode] = {
        uri: courseCode,
        week: -1,
        desc: courseCode
    }

    activities.forEach(activity => {
        // only reflect activity if it is shown on course graph
        for (triple of triples) {
            let involved = [triple.h_name, triple.t_name]
            if (involved.includes(activity.name)) {
                oldData[activity.name] = createItem(activity.desc, activity.name, activity.week)
                break
            }
        }
    });
    let visited = [courseCode, ...firstHop]

    function depthFirst(entity) {
        let children = []
        triples.map(triple => {
            let involved = [triple.h_name, triple.t_name]
            if (involved.includes(entity)) {
                let theOther = [triple.h_name, triple.t_name]
                    .filter(e => e != entity)[0]
                if (!visited.includes(theOther)) {
                    children.push(theOther)
                    visited.push(theOther)
                }
            }
        })
        let result = [entity]
        for (child of children) {
            result = [...result, ...depthFirst(child)]
        }
        return result
    }
    for (firstHopEntity of firstHop) {
        newData[firstHopEntity] = depthFirst(firstHopEntity).filter(e => e != firstHopEntity)
    }
    for (firstHopEntity of firstHop) {
        newData[firstHopEntity] = newData[firstHopEntity].filter(entity => {
            let candidate = activities.filter(a => a.name == entity)
            if (candidate.length == 0) {
                return true
            } else {
                return false
            }
        })
    }
    return [newData, oldData]
}


function assign_timeslot(triples, activities, courseCode) {
    let [newdata,
        olddata
    ] = graph_traversal(triples, activities, courseCode)
    console.log(newdata)
    console.log(olddata)
    let timeslots = {}
    for (let i = 1; i < 14; i++) {
        timeslots[i - .5] = [];
        timeslots[i + ''] = [];
    }
    for (uri in olddata) {
        if (olddata[uri].week < 0) continue;
        let timeSlot = timeslots[olddata[uri].week];
        if (timeSlot) timeSlot.push(olddata[uri]);
    }
    // move item to item
    let noKids = []
    for (firstHopEntity in newdata) {
        if (Object.keys(olddata).includes(firstHopEntity)) {

        } else if (newdata[firstHopEntity].length > 0) {} else {
            noKids.push(firstHopEntity)
        }
    }
    noKids.forEach(firstHopEntityWithNoKids => delete newdata[firstHopEntityWithNoKids])
    newdatakey = Object.keys(newdata)
    newdata[newdatakey[newdatakey.length - 1]] = newdata[newdatakey[newdatakey.length - 1]].concat(noKids)
    // add new data
    let totalItem = 0
    for (firstHopEntity in newdata) {
        totalItem = totalItem + (newdata[firstHopEntity].length < 1 ? 1 : newdata[firstHopEntity].length)
    }
    let slot_cursor = 0

    function couterToRow(c, w, totalItem) {
        return slot_cursor + Math.max(
            Math.min(
                Math.floor(c / (totalItem / w)),
                w - 1
            ),
            0) + 1
    }

    function slot_width(n_item) {
        let num_rows_remining = 13 - slot_cursor
        let itemPerRow = (totalItem / num_rows_remining)
        let width = Math.min(Math.round(n_item / itemPerRow), num_rows_remining)
        totalItem = totalItem - n_item
        return width
    }
    let counter = 0
    for (firstHopEntity in newdata) {
        if (Object.keys(olddata).includes(firstHopEntity)) {

        } else if (newdata[firstHopEntity].length > 0) {
            let width = slot_width(newdata[firstHopEntity].length)
            console.log("new region: " + firstHopEntity)
            console.log(slot_cursor)
            console.log(width)
            for (depthFirstEntity of newdata[firstHopEntity]) {
                let uri = depthFirstEntity,
                    content = depthFirstEntity;
                let slot = couterToRow(counter, width, newdata[firstHopEntity].length)
                console.log(depthFirstEntity)
                console.log(slot)
                let timeSlot = timeslots[slot];
                entity = createItem(content, uri, undefined);
                timeSlot.push(entity);
                counter++
            }
            let uri = firstHopEntity,
                content = firstHopEntity;
            let slot = (slot_cursor + 0.5).toString()
            let timeSlot = timeslots[slot];
            entity = createItem(content, uri, undefined);
            timeSlot.push(entity);
            slot_cursor += width
            if (width > 0) counter = 0
        } else {}
    }
    return timeslots
}


function createItem(content, uri, week) {
    var item = {
        "name": uri,
        "desc": content,
        "week": week
    };
    return item;
}