reactions_solids = [ # Reaction: solid allways negative coefficient!
    {
        "CaCO3(s)": -1.0,
        "CO3--": 1.0,
        "Ca++": 1.0,
        "log_K25": -8.48,
        "log_K_coefs": [
            -171.9065,
            -0.077993,
            2839.319,
            71.595
        ],
        "type": "rev",
        "phase_name": "Calcite"
    },
    {
        "CaCO3(s)": -1.0,
        "CO3--": 1.0,
        "Ca++": 1.0,
        "log_K25": -8.336,
        "log_K_coefs": [
            -171.9773,
            -0.077993,
            2903.293,
            71.595
        ],
        "type": "rev",
        "phase_name": "Aragonite"
    },
    { # Added CM: based on witens.dat (stimela.dat): TODO check log_K25 = aragonite
        "CaCO3(s)": -1.0,
        "CO3--": 1.0,
        "Ca++": 1.0,
        "log_K25": -8.336,
        "log_K_coefs": [
            -172.1295,
            -0.077993,
            3074.688,
            71.595
        ],
        "type": "rev",
        "phase_name": "Vaterite"
    },
    {
        "CaMg(CO3)2(s)": -1.0,
        "Ca++": 1.0,
        "Mg++": 1.0,
        "CO3--": 2.0,
        "log_K25": -17.09,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Dolomite"
    },
    {
        "FeCO3(s)": -1.0,
        "Fe++": 1.0,
        "CO3--": 1.0,
        "log_K25": -10.89,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Siderite"
    },
    {
        "BaCO3(s)": -1.0,
        "Ba++": 1.0,
        "CO3--": 1.0,
        "log_K25": -8.562,
        "log_K_coefs": [
            607.642,
            0.121098,
            -20011.25,
            -236.4948
        ],
        "type": "rev",
        "phase_name": "Witherite"
    },
    {
        "BaSO4(s)": -1.0,
        "Ba++": 1.0,
        "SO4--": 1.0,
        "log_K25": -9.97,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Barite"
    },
    {
        "CaSO4(s)": -1.0,
        "Ca++": 1.0,
        "SO4--": 1.0,
        "log_K25": -4.36,
        "log_K_coefs": [
            84.9,
            0.0,
            -3135.12,
            -31.79
        ],
        "type": "rev",
        "phase_name": "Anhydrite"
    },
    {
        "NaCl(s)": -1.0,
        "Cl-": 1.0,
        "Na+": 1.0,
        "log_K25": 1.57,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Halite"
    },
    {
        "Mn(OH)2(s)": -1.0,
        "H+": -2.0,
        "Mn++": 1.0,
        "H2O": 2.0,
        "log_K25": 15.2,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Pyrochroite"
    },
    {
        "MnCO3(s)": -1.0,
        "Mn++": 1.0,
        "CO3--": 1.0,
        "log_K25": -11.13, #  phreeqc
        #  "log_K25": -10.39, #  wateq
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Rhodochrosite"
    },
    {
        "CaSO4:2H2O(s)": -1.0,
        "Ca++": 1.0,
        "SO4--": 1.0,
        "H2O": 2.0,
        "log_K25": -4.58,
        "log_K_coefs": [
            68.2401,
            0.0,
            -3221.51,
            -25.0627
        ],
        "type": "rev",
        "phase_name": "Gypsum"
    },
    {
        "SrCO3(s)": -1.0,
        "Sr++": 1.0,
        "CO3--": 1.0,
        "log_K25": -9.271,
        "log_K_coefs": [
            155.0305,
            0.0,
            -7239.594,
            -56.58638
        ],
        "type": "rev",
        "phase_name": "Strontianite"
    },
    {
        "SrSO4(s)": -1.0,
        "Sr++": 1.0,
        "SO4--": 1.0,
        "log_K25": -6.63,
        "log_K_coefs": [
            -7.14,
            0.00611,
            75.0,
            0.0,
            0.0,
            -1.79e-05
        ],
        "type": "rev",
        "phase_name": "Celestite"
    },
    {
        "Ca5(PO4)3(OH)(s)": -1.0,
        "H+": -4.0,
        "H2O": 1.0,
        "HPO4--": 3.0,
        "Ca++": 5.0,
        "log_K25": -3.421,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Hydroxyapatite"
    },
    {
        "CaF2(s)": -1.0,
        "Ca++": 1.0,
        "F-": 2.0,
        "log_K25": -10.6,
        "log_K_coefs": [
            66.348,
            0.0,
            -4298.2,
            -25.271
        ],
        "type": "rev",
        "phase_name": "Fluorite"
    },
    {
        "SiO2(s)": -1.0,
        "H2O": -2.0,
        "H4SiO4": 1.0,
        "log_K25": -2.71,
        "log_K_coefs": [
            -0.26,
            0.0,
            -731.0
        ],
        "type": "rev",
        "phase_name": "SiO2(a)"
    },
    {
        "SiO2(s)": -1.0,
        "H2O": -2.0,
        "H4SiO4": 1.0,
        "log_K25": -3.55,
        "log_K_coefs": [
            -0.09,
            0.0,
            -1032.0
        ],
        "type": "rev",
        "phase_name": "Chalcedony"
    },
    {
        "SiO2(s)": -1.0,
        "H2O": -2.0,
        "H4SiO4": 1.0,
        "log_K25": -3.98,
        "log_K_coefs": [
            0.41,
            0.0,
            -1309.0
        ],
        "type": "rev",
        "phase_name": "Quartz"
    },
    {
        "Al(OH)3(s)": -1.0,
        "H+": -3.0,
        "Al+++": 1.0,
        "H2O": 3.0,
        "log_K25": 8.11,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Gibbsite"
    },
    {
        "Al(OH)3(s)": -1.0,
        "H+": -3.0,
        "Al+++": 1.0,
        "H2O": 3.0,
        "log_K25": 10.8,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Al(OH)3(a)"
    },
    {
        "Al2Si2O5(OH)4(s)": -1.0,
        "H+": -6.0,
        "H2O": 1.0,
        "H4SiO4": 2.0,
        "Al+++": 2.0,
        "log_K25": 7.435,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Kaolinite"
    },
    {
        "NaAlSi3O8(s)": -1.0,
        "H2O": -8.0,
        "Na+": 1.0,
        "Al(OH)4-": 1.0,
        "H4SiO4": 3.0,
        "log_K25": -18.002,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Albite"
    },
    {
        "CaAl2Si2O8(s)": -1.0,
        "H2O": -8.0,
        "Ca++": 1.0,
        "Al(OH)4-": 2.0,
        "H4SiO4": 2.0,
        "log_K25": -19.714,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Anorthite"
    },
    {
        "Ca0.165Al2.33Si3.67O10(OH)2(s)": -1.0,
        "H2O": -12.0,
        "Ca++": 0.165,
        "Al(OH)4-": 2.33,
        "H4SiO4": 3.67,
        "H+": 2.0,
        "log_K25": -45.027,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Ca-Montmorillonite"
    },
    {
        "KAlSi3O8(s)": -1.0,
        "H2O": -8.0,
        "K+": 1.0,
        "Al(OH)4-": 1.0,
        "H4SiO4": 3.0,
        "log_K25": -20.573,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "K-feldspar"
    },
    {
        "KCl(s)": -1.0,
        "K+": 1.0,
        "Cl-": 1.0,
        "log_K25": 0.9,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Sylvite"
    },
    {
        "KAl3Si3O10(OH)2(s)": -1.0,
        "H+": -10.0,
        "K+": 1.0,
        "Al+++": 3.0,
        "H4SiO4": 3.0,
        "log_K25": 12.703,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "K-mica"
    },
    {
        "Mg5Al2Si3O10(OH)8(s)": -1.0,
        "H+": -16.0,
        "Mg++": 5.0,
        "Al+++": 2.0,
        "H4SiO4": 3.0,
        "H2O": 6.0,
        "log_K25": 68.38,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Chlorite(14A)"
    },
    {
        "Mg3Si2O5(OH)4(s)": -1.0,
        "H+": -6.0,
        "H2O": 1.0,
        "H4SiO4": 2.0,
        "Mg++": 3.0,
        "log_K25": 32.2,
        "log_K_coefs": [
            13.248,
            0.0,
            10217.1,
            -6.1894
        ],
        "type": "rev",
        "phase_name": "Chrysotile"
    },
    {
        "Mg2Si3O7.5OH:3H2O(s)": -1.0,
        "H+": -4.0,
        "H2O": -0.5,
        "Mg++": 2.0,
        "H4SiO4": 3.0,
        "log_K25": 15.76,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Sepiolite"
    },
    {
        "Mg2Si3O7.5OH:3H2O(s)": -1.0,
        "H+": -4.0,
        "H2O": -0.5,
        "Mg++": 2.0,
        "H4SiO4": 3.0,
        "log_K25": 18.66,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Sepiolite(d)"
    },
    {
        "Mg3Si4O10(OH)2(s)": -1.0,
        "H2O": -4.0,
        "H+": -6.0,
        "Mg++": 3.0,
        "H4SiO4": 4.0,
        "log_K25": 21.399,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Talc"
    },
    {
        "Fe2O3(s)": -1.0,
        "H+": -6.0,
        "Fe+++": 2.0,
        "H2O": 3.0,
        "log_K25": -4.008,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Hematite"
    },
    {
        "KAl3(SO4)2(OH)6(s)": -1.0,
        "H+": -6.0,
        "K+": 1.0,
        "Al+++": 3.0,
        "SO4--": 2.0,
        "H2O": 6.0,
        "log_K25": -1.4,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Alunite"
    },
    {
        "Fe(OH)3(s)": -1.0,
        "H+": -3.0,
        "Fe+++": 1.0,
        "H2O": 3.0,
        "log_K25": 4.891,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Fe(OH)3(a)"
    },
    {
        "FeS(s)": -1.0,
        "H+": -1.0,
        "Fe++": 1.0,
        "HS-": 1.0,
        "log_K25": -3.915,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "FeS(ppt)"
    },
    {
        "FeS(s)": -1.0,
        "H+": -1.0,
        "Fe++": 1.0,
        "HS-": 1.0,
        "log_K25": -4.648,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Mackinawite"
    },
    {
        "S(s)": -1.0,
        "H+": -2.0,
        "e-": -2.0,
        "H2S": 1.0,
        "log_K25": 4.882,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Sulfur"
    },
    {
        "Fe(OH)3(s)": -1.0,
        "H+": -3.0,
        "Fe+++": 1.0,
        "H2O": 3.0,
        "log_K25": 4.891,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Fe(OH)3(a)"
    },
    {
        "MnO2:H2O(s)": -1.0,
        "H+": -4.0,
        "e-": -2.0,
        "Mn++": 1.0,
        "H2O": 3.0,
        "log_K25": 41.38,
        "log_K_coefs": "",
        "type": "electronic",
        "phase_name": "Pyrolusite"
    },
    {
        "FeS2(s)": -1.0,
        "H+": -2.0,
        "e-": -2.0,
        "Fe++": 1.0,
        "HS-": 2.0,
        "log_K25": -18.479,
        "log_K_coefs": "",
        "type": "electronic",
        "phase_name": "Pyrite"
    },
    {
        "FeOOH(s)": -1.0,
        "H+": -3.0,
        "Fe+++": 1.0,
        "H2O": 2.0,
        "log_K25": -1.0,
        "log_K_coefs": "",
        "type": "rev",
        "phase_name": "Goethite"
    }
]
