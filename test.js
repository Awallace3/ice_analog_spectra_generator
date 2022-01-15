

d = {
    buildGeoms: {
        enable: true,
        dataPath: "data/48_1_1_h2o_nh3",
        inputCartesianFiles: [
            {
                file: "h2o.txt",
                count: 24
            },
            {
                file: "nh3.txt",
                count: 24
            }
        ],
        clusters: 48,
        boxLength: 12,
        minDistanceMolecules: 3,
        optMethod: "B3LYP",
        optBasisSet: "6-31G(d)",
        memComFile: "1600",
        memPBSFile: "15",
        nProcs: "4"
    },
    jobResubmit: {
        enable: {
            exc: true,
            vib: false
        },
        qmgr: {
            minDelay: 360,
            maxResub: 100
        },
        optResub: {
            optMethod: "B3LYP",
            optBasisSet: "6-31G(d)",
            memComFile: "1600",
            memPBSFile: "15"
        },
        excCreate: [
                {
                    excMethod: "CAM-B3LYP",
                    excBasisSet: "6-31G(d)",
                    memComFile: "1600",
                    memPBSFile: "15",
                    nStates: 25,
                    SCRF: ""
                },
                {
                    excMethod: "CAM-B3LYP",
                    excBasisSet: "6-311G(d,p)",
                    memComFile: "1600",
                    memPBSFile: "15",
                    nStates: 50,
                    SCRF: ""
                },
                {
                    excMethod: "wB97XD",
                    excBasisSet: "6-31G(d)",
                    memComFile: "1600",
                    memPBSFile: "15",
                    nStates: 25,
                    SCRF: ""
                }
            ],
        vibCreate: [
                {
                    excMethod: "CAM-B3LYP",
                    excBasisSet: "6-31+G(d,p)",
                    memComFile: "1600",
                    memPBSFile: "15"
                }
        ]
    },
    dataAnalysis: {
        enable: true,
        temperature: 273.15,
        type: "exc",
        output: {
            numerical: {
                enable: true,
                type: "json",
                outFile: "tmp.json"
            },
            plot: {
                enable: true,
                range: {
                    x: [1, 12],
                    y: [0, 1]
                },
                expData: [
                    {
                        path: "../expData/exp1.txt",
                        units: {
                            input: "nm",
                            output: "eV"
                        },
                        line: {
                            color: "black",
                            type: "dotted"
                        }
                    },
                    {
                        path: "../expData/exp2.txt",
                        units: {
                            input: "nm",
                            output: "eV"
                        },
                        line: {
                            color: "black",
                            type: "line"
                        }
                    }
                ]
            }
        },
        excList: [
                {
                    excMethod: "CAM-B3LYP",
                    excBasisSet: "6-31G(d)",
                    nStates: 25,
                    SCRF: ""
                },
                {
                    excMethod: "wB97XD",
                    excBasisSet: "6-31G(d)",
                    nStates: 25,
                    SCRF: ""
                }
            ]
    }
}

console.log(JSON.stringify(d))
