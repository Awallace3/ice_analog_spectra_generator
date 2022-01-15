import json
import src


def main():
    with open("input.json") as f:
        config = json.load(f)

    if config["buildGeoms"]["enable"]:
        src.ice_build(config=config["buildGeoms"])

    if config["jobResubmit"]["enable"]["exc"]:
        complete = src.jobResubmit(config["jobResubmit"])

    if (
        config["dataAnalysis"]["enable"]
        and config["dataAnalysis"]["output"]["plot"]["enable"]
    ):
        src.electronicMultiPlotExpSetup(config["dataAnalysis"])


    """
    boltzmannAnalysisSetup(complete, method_mexc, nStates=nStates)
    gather_energies.main()

    boltzmannAnalysis(T)
    generateGraph("spec", T, title, filename, x_range=[5,10], x_units='ev', peaks=True)
    ### NH3 6-311++G(d,p) need to test nstates==50

    # to combine total electronic calculations
    methods_lst = ["B3LYP", "PBE0", "wB97XD", "CAM-B3LYP", "B3LYPD3", "B97D3"]

    methods_lst = ["B3LYP", "PBE0", "wB97XD", "CAM-B3LYP", "B97D3"]
    colors = ["blue", "orange", "green", "red", "cyan"]
    # methods_lst = ["CAM-B3LYP"]
    colors = ["red", "green"]
    methods_lst = ["CAM-B3LYP", "wB97XD"]
    methods_lst = ["CAM-B3LYP"]
    # methods_lst = []
    colors = ["red", "green"]
    # methods_lst = ["CAM-B3LYP", "wB97XD"]
    # colors = ["red", 'green']
    # methods_lst = ["B3LYP"]
    # colors = ["blue"]

    title = (
        r"30 Randomized Clusters of 8 %s Molecules with %s"
        % (
            moleculeNameLatex,
            basis_dir_name[1:].replace(nStates, ""),
        )
        + "\nat N=%s and T=%s K" % (nStates, T)
    )
    filename = "30_8_%s_elec_n%s_%s_%sK.pdf" % (
        moleculeName,
        nStates,
        basis_dir_name[1:].replace(nStates, ""),
        T,
    )
    if len(methods_lst) == 1:
        filename = "30_8_%s_elec_%s_n%s_%s_%sK.pdf" % (
            moleculeName,
            method_mexc,
            nStates,
            basis_dir_name[1:].replace(nStates, ""),
            T,
        )
    # filename = "30_8_%s_test_%sk.pdf" % ( moleculeName, T)

    filename = "30_8_%s_elec_n%s_%s_%sK.pdf" % (
        moleculeName,
        nStates,
        basis_set_mexc,
        T,
    )
    filename = "30_8_%s_elec_n%s_%s_%sK.png" % (
        moleculeName,
        nStates,
        basis_set_mexc,
        T,
    )
    title = (
        r"30 Randomized Clusters of 8 %s Molecules with %s"
        % (moleculeNameLatex, basis_set_mexc)
        + "\nat %s K" % T
    )

    # methods_lst = method_update_selection(methods_lst, basis_set_mexc, nStates)
    # print(methods_lst)

    acquiredStates = nStates
    # acquiredStates = '15'
    filename = "30_8_%s_elec_n%s_%s_%sK_exp.pdf" % (
        moleculeName,
        nStates,
        basis_set_mexc,
        T,
    )
    filename = "30_8_%s_elec_n%s_%s_%sK_exp.png" % (
        moleculeName,
        nStates,
        basis_set_mexc,
        T,
    )
    title = (
        r"30 Randomized Clusters of 8 %s Molecules with %s"
        % (moleculeNameLatex, basis_set_mexc)
        + "\nat %s K compared with experiment" % T
    )
    title = ""
    filename = "30_8_%s_elec_n%s_%s_%sK_exp_STATES.png" % (
        moleculeName,
        nStates,
        basis_set_mexc,
        T,
    )
    # filename = "30_8_%s_elec_n%s_%s_%sK_exp_STATES_%s_B.png" % ( moleculeName, nStates, basis_set_mexc , T, acquiredStates)
    if SCRF != "":
        filename = "30_8_%s_elec_n%s_%s_%sK_exp_STATES_%s_%s.png" % (
            moleculeName,
            nStates,
            basis_set_mexc,
            T,
            acquiredStates,
            SCRF,
        )

    # co3h2 start
    exp_solid1 = np.genfromtxt('../../exp_data/%s_200k.csv'% moleculeName, delimiter=', ')
    exp_solid1 = nmLst_evLst(exp_solid1)
    exp_solid2 = np.genfromtxt('../../exp_data/%s_80_200k.csv'% moleculeName, delimiter=', ')
    exp_solid2 = nmLst_evLst(exp_solid2)
    #exp_data = [ exp_solid ]
    exp_data = [exp_solid1, exp_solid2]
    #exp_data = [ exp_solid2 ]
    #print(exp_da#ta)
    
    #octa_rib = dis_art.discrete_to_art('../ribbon/8rib_cam.dat', ['nm', 'eV'], [100, 320], 2)
    # co3h2 end
    exp_solid1 = np.genfromtxt("../../exp_data/%s_solid.csv" % moleculeName, delimiter=", ")
    #exp_solid1 = nmLst_evLst(exp_solid1)
    exp_data=[exp_solid1]

    electronicMultiPlot_Experiment(
        methods_lst,
        T,
        title,
        filename,
        x_range=[7, 10.25],
        x_units="eV",
        peaks=True,
        spec_name="spec",
        complete=complete,
        basis_set_mexc=basis_set_mexc,
        nStates=nStates,
        acquiredStates=acquiredStates,
        exp_data=exp_data,
        colors=colors,
        sec_y_axis=True,
        rounding=2,
        # extra_data=octa_rib,
        SCRF=SCRF,
    )
    print("OUTPUT =\n", filename)

    # method_vib = "M062X"
    method_vib = "CAM-B3LYP"
    # basis_set_vib = "6-31+G(d,p)"
    basis_set_vib = "aug-cc-pVDZ"
    mem_com_vib = mem_com_opt 
    mem_pbs_vib = mem_pbs_opt
    overall_name = '8_nh3'

    vibrational_resubmit(
            resubmit_delay_min, resubmit_max_attempts,
            method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
            method_vib, basis_set_vib, mem_com_vib, mem_pbs_vib,
            SCRF=SCRF, overall_name=overall_name
    )

    overTones = False
    overTonesBoltzmannAnalysis = True
    if overTones: 
        filename = "30_8_rand_%s_vib_wB97XD_overtones.png" % moleculeName
        title = "30 8 rand %s with overtones" % moleculeName
    else: 
        filename = "30_8_rand_%s_vib_wB97XD_none.png" % moleculeName
        title = "30 8 rand %s with no" % moleculeName

    if overTonesBoltzmannAnalysis:
        filename = "30_8_rand_%s_vib_wB97XD_overtones_from_maximas.png" % moleculeName
    # for vibrational frequency standard usage

    vibrational_frequencies.main(overTones, T=500)
    boltzmannAnalysis(T, energy_levels='vibrational', DeltaN='10', x_range=[50, 4100], overtones=overTonesBoltzmannAnalysis)
    generateGraph("spec", T, title, filename, x_range=[4000, 400], x_units='cm-1', peaks=False)
    """

    # useful bash commands below
    # ps aux | grep test.py
    # kill <pid> -9
    # python3 -u ./ice_manager.py > output.log & disown -h


if __name__ == "__main__":
    main()
