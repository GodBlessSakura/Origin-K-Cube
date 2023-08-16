//{% macro script() %}
function flattenSchedule(schedule) {
    return Object.keys(schedule).reduce((previous, current) => {
        return previous.concat(schedule[current])
    }, [])
}

function recursiveSearch(tree, name) {
    if (tree.name == name) return tree
    for (const child of flattenSchedule(tree.schedule)) {
        let value = recursiveSearch(child, name)
        if (value != null) return value
    }
    return null
}

function traversal(name, triples, activities) {
    let activity = activities.filter(a => a.name == name)
    // {% if request.blueprint != "instructor" and request.blueprint != "DLTC"  %}
    if (activities.length == 0) return null
    // {% endif %}
    let node = {
        name: name,
        desc: activity.length > 0 ? activity[0].desc : name,
        week: activity.length > 0 ?
            (Number.isInteger(Number(activity[0].week)) ? Number(activity[0].week) : null) : null,
        children: []
    }
    triples = triples.filter(triple => {
        if (triple.t_name == name) {
            node.children.push(triple.h_name)
            return false
        }
        return true
    })
    triples = triples.filter(triple => { // do for remove mutli path
        if (node.children.includes(triple.h_name)) {
            return false
        }
        return true
    })
    node.children = node.children.map(child => traversal(child, triples, activities))
    return node
}

function flattenListOfNode(nodes) {
    return [...nodes, ...nodes.flatMap(n => {
        let children = flattenSchedule(n.schedule)
        return [...children, ...children.length > 0 ? flattenListOfNode(children) : []]
    })]
}

function sortChildren(node) {
    if (node.children.length == 0) {
        node.numItem = 1
    } else {
        node.children.forEach(child => (sortChildren(child)))
        node.children = node.children.sort((childA, childB) => {
            if (childA.week != null && childB.week != null) {
                return childA.week - childB.week
            } else if (childA.week != null & childB.week == null) {
                return -1
            } else if (childA.week == null & childB.week != null) {
                return 1
            } else {
                return childB.numItem - childA.numItem
            }
        })
        node.children.forEach(child => child.parent = node)
        node.numItem = node.children.map(child => child.numItem).reduce((previous, current) => previous + current)
    }
}

function allocate(node, slot, totalItem) {
    node.notSync = false
    if (node.week === null) {
        node.notSync = true
        node.week = Math.min(Math.round(slot * weekInSemester) + 1, weekInSemester)
    }
    if (node.children.length == 0) {
        slot = slot + 1 / totalItem
    }
    node.children.forEach(child => {
        slot = allocate(child, slot, totalItem)
    })
    node.schedule = node.children.reduce(
        (previous, child) => {
            if (previous[child.week]) {
                previous[child.week].push(child)
            } else {
                previous[child.week] = [child]
            }
            return previous
        }, Object.create(null))
    delete node.children
    return slot
}
//{% endmacro %}