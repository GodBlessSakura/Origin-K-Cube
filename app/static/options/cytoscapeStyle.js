var cyStylesOptionsDefault = {
    editor: {
        "font-size": 12,
        "node-color": KCube.colorTheme.info,
        "line-color": KCube.colorTheme.info,
        "selected-color": KCube.colorTheme.success,
        "background-color": '#ffffff',
        'node-size': 17.5,
        showDefaultRelationLabel: false,
        showNodeLabel: true,
    },
    viewer: {
        "font-size": 12,
        "node-color": KCube.colorTheme.info,
        "line-color": KCube.colorTheme.info,
        "selected-color": KCube.colorTheme.success,
        "background-color": '#ffffff',
        'node-size': 17.5,
        showDefaultRelationLabel: false,
        showNodeLabel: true,
    },
}
var cyStylesOptions = {}
var cyStylesUtil = {
    getLocal: () => {
        let option = localStorage.getItem('cyStylesOptions')
        if (option != null) cyStylesOptions = JSON.parse(option)
    },
    setLocal: () => {
        let option = JSON.stringify(cyStylesOptions)
        console.log(option)
        localStorage.setItem('cyStylesOptions', option)
    },
    setDefault: () => {
        cyStylesOptions = JSON.parse(JSON.stringify(cyStylesOptionsDefault))
    }

}
cyStylesUtil.setDefault()
cyStylesUtil.getLocal()
var cyStyles = {
    get simpleStyle() {
        options = cyStylesOptions.viewer
        return [{
                selector: 'background-color',
                style: {
                    'background-color': options["background-color"],
                }
            }, {
                selector: 'node',
                style: {
                    'height': options["node-size"],
                    'width': options["node-size"],
                    'label': options.showNodeLabel ? 'data(name)' : '',
                    'text-max-width': 120,
                    'text-wrap': 'ellipsis',
                    'font-size': options["font-size"],
                    'background-color': options["node-color"],
                    'background-image': 'data(imageURL)',
                    'background-fit': 'cover'
                }
            },
            {
                selector: 'edge',
                style: {
                    'label': 'data(name)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'font-size': options["font-size"],
                    'text-rotation': 'autorotate',
                    'line-style': 'solid',
                    'line-color': options["line-color"],
                    'target-arrow-color': options["line-color"],
                    'width': 2,
                }
            },
            {
                selector: ':selected',
                style: {
                    'color': options["selected-color"],
                    'line-color': options["selected-color"],
                    'background-color': options["selected-color"],
                    'target-arrow-color': options["selected-color"],
                }
            },
        ].concat(!options.showDefaultRelationLabel ? {
            selector: 'edge[name = "Subtopic in"]',
            style: {
                label: ''
            }
        } : [])
    },
    get basicEditStyle() {
        options = cyStylesOptions.editor
        return [{
                selector: 'background-color',
                style: {
                    'background-color': options["background-color"],
                }
            }, {
                selector: 'node',
                style: {
                    'height': options["node-size"],
                    'width': options["node-size"],
                    'label': options.showNodeLabel ? 'data(name)' : '',
                    'text-max-width': 120,
                    'text-wrap': 'ellipsis',
                    'font-size': options["font-size"],
                    'background-color': options["node-color"],
                    'background-fit': 'cover'
                }
            }, {
                selector: 'node[imageURL]',
                style: {
                    'background-image': 'data(imageURL)',
                }
            },
            {
                selector: 'node.tempory',
                style: {
                    'opacity': 0.25,
                }
            },
            {
                selector: 'edge',
                style: {
                    'label': 'data(name)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'font-size': options["font-size"],
                    'text-rotation': 'autorotate',
                    'display': 'none',
                    'line-color': options["line-color"],
                    'target-arrow-color': options["line-color"],
                }
            }, {
                selector: 'edge[subject_value = "true"][workspace_value != "false"],[workspace_value = "true"]',
                style: {
                    'line-style': 'solid',
                    'width': 3,
                    'display': 'element',
                }
            },
            {
                selector: ':selected',
                style: {
                    'color': options["selected-color"],
                    'line-color': options["selected-color"],
                    'background-color': options["selected-color"],
                    'target-arrow-color': options["selected-color"],
                }
            },
        ].concat(!options.showDefaultRelationLabel ? {
            selector: 'edge[name = "Subtopic in"]',
            style: {
                label: ''
            }
        } : [])
    },
    get diffEditStyle() {
        options = cyStylesOptions.editor
        return [{
                selector: 'background-color',
                style: {
                    'background-color': options["background-color"],
                }
            }, {
                selector: 'node',
                style: {
                    'height': options["node-size"],
                    'width': options["node-size"],
                    'label': options.showNodeLabel ? 'data(name)' : '',
                    'text-max-width': 120,
                    'text-wrap': 'ellipsis',
                    'font-size': options["font-size"],
                    'background-color': options["node-color"],
                    'background-image': 'data(imageURL)',
                    'background-fit': 'cover'
                }
            }, {
                selector: 'edge.suppress',
                style: {
                    'opacity': 0.15,
                }
            },
            {
                selector: 'node.tempory',
                style: {
                    'opacity': 0.25,
                }
            },
            {
                selector: 'edge',
                style: {
                    'label': 'data(name)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'font-size': options["font-size"],
                    'text-rotation': 'autorotate',
                    'width': 3,
                    'line-color': options["line-color"],
                    'target-arrow-color': options["line-color"],
                }
            }, {
                selector: 'edge[workspace_value = "true"][subject_value != "true"]',
                style: {
                    'line-style': 'solid',
                    'font-weight': 'bold',
                }
            }, {
                selector: 'edge[workspace_value = "false"][subject_value = "true"]',
                style: {
                    'line-gradient-stop-colors': [options["line-color"],
                        options["background-color"],
                        options["background-color"],
                        options["line-color"]
                    ].join(' '),
                    'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                    'line-fill': 'linear-gradient ',
                    'font-weight': 'bold',
                }
            }, {
                selector: 'edge[workspace_value = "true"][subject_value = "true"]',
                style: {
                    'line-style': 'solid',
                    'text-outline-color': 'black',
                    'text-outline-width': 0.25,
                    'color': 'white',
                }
            }, {
                selector: 'edge[workspace_value = "false"][subject_value != "true"]',
                style: {
                    'line-gradient-stop-colors': [options["line-color"],
                        options["background-color"],
                        options["background-color"],
                        options["line-color"]
                    ].join(' '),
                    'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                    'line-fill': 'linear-gradient ',
                    'text-outline-color': 'black',
                    'text-outline-width': 0.25,
                    'color': 'white',
                }
            }, {
                selector: 'edge[workspace_value = "false"][subject_value != "true"]:selected',
                style: {
                    'text-outline-color': options["selected-color"],
                }
            }, {
                selector: 'edge[workspace_value = "undefined"][subject_value = "true"]',
                style: {
                    'line-style': 'solid',
                }
            }, {
                selector: 'edge[workspace_value = "undefined"][subject_value = "false"]',
                style: {
                    'line-style': 'dashed',
                    'line-dash-pattern': '10%, 80%',
                }
            },
            {
                selector: ':selected',
                style: {
                    'color': options["selected-color"],
                    'line-color': options["selected-color"],
                    'background-color': options["selected-color"],
                    'target-arrow-color': options["selected-color"],
                    'line-gradient-stop-colors': [options["selected-color"],
                        options["background-color"],
                        options["background-color"],
                        options["selected-color"]
                    ].join(' '),
                }
            },
        ].concat(!options.showDefaultRelationLabel ? {
            selector: 'edge[name = "Subtopic in"]',
            style: {
                label: ''
            }
        } : [])
    },
    get previewStyle() {
        options = cyStylesOptions.viewer
        return [{
                selector: 'background-color',
                style: {
                    'background-color': options["background-color"],
                }
            }, {
                selector: 'node',
                style: {
                    'height': options["node-size"],
                    'width': options["node-size"],
                    'label': options.showNodeLabel ? 'data(name)' : '',
                    'text-max-width': 120,
                    'text-wrap': 'ellipsis',
                    'font-size': options["font-size"],
                    'background-color': options["node-color"],
                    'background-image': 'data(imageURL)',
                    'background-fit': 'cover'
                }
            },
            {
                selector: 'edge',
                style: {
                    'label': 'data(name)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'font-size': options["font-size"],
                    'text-rotation': 'autorotate',
                    'line-style': 'solid',
                    'line-color': options["line-color"],
                    'target-arrow-color': options["line-color"],
                    'opacity': 0
                }
            }, {
                selector: 'edge[preview_value != "false"][original_value = "true"]',
                style: {
                    'line-style': 'solid',
                    'width': 1,
                    'opacity': 0.25
                }
            }, {
                selector: 'edge[preview_value != "true"][original_value = "false"]',
                style: {
                    'line-gradient-stop-colors': [options["line-color"],
                        options["background-color"],
                        options["background-color"],
                        options["line-color"]
                    ].join(' '),
                    'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                    'line-fill': 'linear-gradient ',
                    'width': 1,
                    'opacity': 0.25
                }
            },
            {
                selector: 'edge[preview_value = "false"][original_value = "true"]',
                style: {
                    'line-gradient-stop-colors': [options["line-color"],
                        options["background-color"],
                        options["background-color"],
                        options["line-color"]
                    ].join(' '),
                    'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                    'line-fill': 'linear-gradient ',
                    'width': 5,
                    'opacity': 1
                }
            },
            {
                selector: 'edge[preview_value = "true"][original_value = "false"]',
                style: {
                    'width': 5,
                    'opacity': 1
                }
            },
            {
                selector: 'edge[preview_value = "true"][original_value = "undefined"]',
                style: {
                    'width': 5,
                    'opacity': 1
                }
            },
        ].concat(!options.showDefaultRelationLabel ? {
            selector: 'edge[name = "Subtopic in"]',
            style: {
                label: ''
            }
        } : [])
    },
    get subjectStyle() {
        options = cyStylesOptions.viewer
        return [{
                selector: 'background-color',
                style: {
                    'background-color': options["background-color"],
                }
            }, {
                selector: 'node',
                style: {
                    'height': options["node-size"],
                    'width': options["node-size"],
                    'label': options.showNodeLabel ? 'data(name)' : '',
                    'text-max-width': 120,
                    'text-wrap': 'ellipsis',
                    'font-size': options["font-size"],
                    'background-color': options["node-color"],
                    'background-image': 'data(imageURL)',
                    'background-fit': 'cover'
                }
            },
            {
                selector: 'edge',
                style: {
                    'label': 'data(name)',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'font-size': options["font-size"],
                    'text-rotation': 'autorotate',
                    'line-style': 'solid',
                    'line-color': options["line-color"],
                    'target-arrow-color': options["line-color"],
                    'opacity': 0
                }
            }, {
                selector: 'edge[original_value = "true"]',
                style: {
                    'line-style': 'solid',
                    'width': 1,
                    'opacity': 1
                }
            }, {
                selector: 'edge[original_value = "false"]',
                style: {
                    'line-gradient-stop-colors': [options["line-color"],
                        options["background-color"],
                        options["background-color"],
                        options["line-color"]
                    ].join(' '),
                    'line-gradient-stop-positions': '10% 10% 77.5% 77.5%',
                    'line-fill': 'linear-gradient ',
                    'width': 1,
                    'opacity': 1
                }
            },
        ].concat(!options.showDefaultRelationLabel ? {
            selector: 'edge[name = "Subtopic in"]',
            style: {
                label: ''
            }
        } : [])
    }
}