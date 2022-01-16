import json
import src


def main():
    with open("input.json") as f:
        config = json.load(f)

    if config["buildGeoms"]["enable"]:
        src.ice_build(config=config["buildGeoms"])

    if config["qmgr"]["enable"]["exc"]:
        src.qmgr(config["qmgr"])

    if (
        config["dataAnalysis"]["enable"]
        and config["dataAnalysis"]["output"]["plot"]["enable"]
    ):
        src.electronicMultiPlotExpSetup(config["dataAnalysis"])

    """
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
