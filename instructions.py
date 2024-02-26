from utils.instructions import _instruction, _rate_instruction


sorv_pass_instructions = [
    #
    # Enterobacterales
    _instruction("sorv_pass", "Sorveglianza passiva", "citspp", "Citrobacter spp"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "enbaco", "Enterobacter cloacae complex"
    ),
    _instruction("sorv_pass", "Sorveglianza passiva", "esccol", "Escherichia coli"),
    _instruction("sorv_pass", "Sorveglianza passiva", "kleoxy", "Klebsiella oxytoca"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "klepne", "Klebsiella pneumoniae"
    ),
    _instruction("sorv_pass", "Sorveglianza passiva", "klespe", "Klebsiella spp"),
    _instruction("sorv_pass", "Sorveglianza passiva", "mormor", "Morganella morganii"),
    _instruction("sorv_pass", "Sorveglianza passiva", "prospp", "Proteus spp"),
    _instruction("sorv_pass", "Sorveglianza passiva", "sermar", "Serratia marcescens"),
    #
    # altri gram negativi
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "acibcx", "Acinetobacter baumannii complex"
    ),
    _instruction("sorv_pass", "Sorveglianza passiva", "psecep", "Burkholderia cepacia"),
    _instruction("sorv_pass", "Sorveglianza passiva", "camspp", "Campylobacter spp"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "pseaer", "Pseudomonas aeruginosa"
    ),
    _instruction("sorv_pass", "Sorveglianza passiva", "psespp", "Pseudomonas spp"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "salgad", "Salmonella gruppo A-D"
    ),
    _instruction("sorv_pass", "Sorveglianza passiva", "shispe", "Shigella spp"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "psemal", "Stenotrophomonas maltophilia"
    ),
    #
    # altri batteri
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "clodif", "Clostridioides difficile"
    ),
    _instruction(
        "sorv_pass",
        "Sorveglianza passiva",
        "legpna",
        "Antigene legionella (L. pneumophila sg. 1)",
    ),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "legpne", "Legionella pneumophila"
    ),
    _instruction(
        "sorv_pass",
        "Sorveglianza passiva",
        "myctuc",
        "Mycobacterium tuberculosis complex",
        cutoff_repeat_days=180,
    ),
    _instruction(
        "sorv_pass",
        "Sorveglianza passiva",
        "mott",
        "Mycobacterium other than tuberculosis",
        cutoff_repeat_days=180,
    ),
    #
    # Gram positivi
    _instruction("sorv_pass", "Sorveglianza passiva", "entspp", "Enterococcus spp"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "staaur", "Staphylococcus aureus"
    ),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "strpna", "Antigene streptococcico"
    ),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "strpne", "Streptococcus pneumoniae"
    ),
    #
    # altri batteri
    _instruction("sorv_pass", "Sorveglianza passiva", "bacant", "Bacillus anthracis"),
    _instruction(
        "sorv_pass", "Sorveglianza passiva", "cordip", "Corynebacterium diphteriae"
    ),
    _instruction("sorv_pass", "Sorveglianza passiva", "vibcho", "Vibrio cholerae"),
    _instruction("sorv_pass", "Sorveglianza passiva", "yerpst", "Yersinia pestis"),
    #
    # virus e funghi
    _instruction("sorv_pass", "Sorveglianza passiva", "nor", "Norovirus"),
    _instruction("sorv_pass", "Sorveglianza passiva", "rtv", "Rotavirus"),
]

sangue_liquor_instructions = [
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "cryneo", "Cryptococcus neoformans"
    ),
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "haeinf", "Haemophilus influenzae"
    ),
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "lismoc", "Listeria monocytogenes"
    ),
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "neimen", "Neisseria meningitidis"
    ),
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "straga", "Streptococcus agalactiae"
    ),
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "strpyo", "Streptococcus pyogenes"
    ),
    _instruction(
        "sangue+liquor", "liquor ed emocolture", "strpne", "Streptococcus pneumoniae"
    ),
]
liquor_instructions = [
    _instruction("liquor", "Liquor", "cryneo", "Cryptococcus neoformans"),
    _instruction("liquor", "Liquor", "haeinf", "Haemophilus influenzae"),
    _instruction("liquor", "Liquor", "lismoc", "Listeria monocytogenes"),
    _instruction("liquor", "Liquor", "neimen", "Neisseria meningitidis"),
    _instruction("liquor", "Liquor", "straga", "Streptococcus agalactiae"),
    _instruction("liquor", "Liquor", "strpyo", "Streptococcus pyogenes"),
    _instruction("liquor", "Liquor", "strpne", "Streptococcus pneumoniae"),
]

sangue_instructions = [
    #
    # Enterobacterales
    _instruction("sangue", "Sangue", "citspp", "Citrobacter spp"),
    _instruction("sangue", "Sangue", "enbaco", "Enterobacter cloacae complex"),
    _instruction("sangue", "Sangue", "esccol", "Escherichia coli"),
    _instruction("sangue", "Sangue", "kleoxy", "Klebsiella oxytoca"),
    _instruction("sangue", "Sangue", "klepne", "Klebsiella pneumoniae"),
    _instruction("sangue", "Sangue", "klespe", "Klebsiella spp"),
    _instruction("sangue", "Sangue", "mormor", "Morganella morganii"),
    _instruction("sangue", "Sangue", "prospp", "Proteus spp"),
    _instruction("sangue", "Sangue", "sermar", "Serratia marcescens"),
    #
    # altri gram negativi
    _instruction("sangue", "Sangue", "acibcx", "Acinetobacter baumannii complex"),
    _instruction("sangue", "Sangue", "haeinf", "Haemophilus influenzae"),
    _instruction("sangue", "Sangue", "neimen", "Neisseria meningitidis"),
    _instruction("sangue", "Sangue", "pseaer", "Pseudomonas aeruginosa"),
    _instruction("sangue", "Sangue", "psespp", "Pseudomonas spp"),
    _instruction("sangue", "Sangue", "psemal", "Stenotrophomonas maltophilia"),
    #
    # altri batteri
    #
    # Gram positivi
    _instruction("sangue", "Sangue", "entspp", "Enterococcus spp"),
    _instruction("sangue", "Sangue", "lismoc", "Listeria monocytogenes"),
    _instruction("sangue", "Sangue", "staaur", "Staphylococcus aureus"),
    _instruction("sangue", "Sangue", "straga", "Streptococcus agalactiae"),
    _instruction("sangue", "Sangue", "strpyo", "Streptococcus pyogenes"),
    _instruction("sangue", "Sangue", "strpne", "Streptococcus pneumoniae"),
    #
    # altri batteri
    #
    # micobatteri
    #
    # funghi
    _instruction("sangue", "Sangue", "canaur", "Candida auris"),
    _instruction("sangue", "Sangue", "canspp", "Candida spp"),
    _instruction("sangue", "Sangue", "cryneo", "Cryptococcus neoformans"),
    #
    # virus
]

urine_instructions = [
    #
    # Enterobacterales
    _instruction("urine", "Urine (tutto)", "citspp", "Citrobacter spp"),
    _instruction("urine", "Urine (tutto)", "enbaco", "Enterobacter cloacae complex"),
    _instruction("urine", "Urine (tutto)", "esccol", "Escherichia coli"),
    _instruction("urine", "Urine (tutto)", "kleoxy", "Klebsiella oxytoca"),
    _instruction("urine", "Urine (tutto)", "klepne", "Klebsiella pneumoniae"),
    _instruction("urine", "Urine (tutto)", "klespe", "Klebsiella spp"),
    _instruction("urine", "Urine (tutto)", "mormor", "Morganella morganii"),
    _instruction("urine", "Urine (tutto)", "prospp", "Proteus spp"),
    _instruction("urine", "Urine (tutto)", "sermar", "Serratia marcescens"),
    #
    # altri gram negativi
    _instruction("urine", "Urine (tutto)", "acibcx", "Acinetobacter baumannii complex"),
    _instruction("urine", "Urine (tutto)", "pseaer", "Pseudomonas aeruginosa"),
    _instruction("urine", "Urine (tutto)", "psespp", "Pseudomonas spp"),
    _instruction("urine", "Urine (tutto)", "psemal", "Stenotrophomonas maltophilia"),
    #
    # altri batteri
    #
    # Gram positivi
    _instruction("urine", "Urine (tutto)", "entspp", "Enterococcus spp"),
    _instruction("urine", "Urine (tutto)", "staaur", "Staphylococcus aureus"),
    #
    # altri batteri
    #
    # micobatteri
    #
    # funghi
    #
    # virus
]

urine_cv_instructions = [
    #
    # Enterobacterales
    _instruction("urine_cv", "Urine (CV)", "citspp", "Citrobacter spp"),
    _instruction("urine_cv", "Urine (CV)", "enbaco", "Enterobacter cloacae complex"),
    _instruction("urine_cv", "Urine (CV)", "esccol", "Escherichia coli"),
    _instruction("urine_cv", "Urine (CV)", "kleoxy", "Klebsiella oxytoca"),
    _instruction("urine_cv", "Urine (CV)", "klepne", "Klebsiella pneumoniae"),
    _instruction("urine_cv", "Urine (CV)", "klespe", "Klebsiella spp"),
    _instruction("urine_cv", "Urine (CV)", "mormor", "Morganella morganii"),
    _instruction("urine_cv", "Urine (CV)", "prospp", "Proteus spp"),
    _instruction("urine_cv", "Urine (CV)", "sermar", "Serratia marcescens"),
    #
    # altri gram negativi
    _instruction("urine_cv", "Urine (CV)", "acibcx", "Acinetobacter baumannii complex"),
    _instruction("urine_cv", "Urine (CV)", "pseaer", "Pseudomonas aeruginosa"),
    _instruction("urine_cv", "Urine (CV)", "psespp", "Pseudomonas spp"),
    _instruction("urine_cv", "Urine (CV)", "psemal", "Stenotrophomonas maltophilia"),
    #
    # altri batteri
    #
    # Gram positivi
    _instruction("urine_cv", "Urine (CV)", "entspp", "Enterococcus spp"),
    _instruction("urine_cv", "Urine (CV)", "staaur", "Staphylococcus aureus"),
    #
    # altri batteri
    #
    # micobatteri
    #
    # funghi
    #
    # virus
]

respiratorio_instructions = [
    #
    # Enterobacterales
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "citspp", "Citrobacter spp"
    ),
    _instruction(
        "respiratorio",
        "Respiratorio (BAL+BAS+ESP)",
        "enbaco",
        "Enterobacter cloacae complex",
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "esccol", "Escherichia coli"
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "kleoxy", "Klebsiella oxytoca"
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "klepne", "Klebsiella pneumoniae"
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "klespe", "Klebsiella spp"
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "mormor", "Morganella morganii"
    ),
    _instruction("respiratorio", "Respiratorio (BAL+BAS+ESP)", "prospp", "Proteus spp"),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "sermar", "Serratia marcescens"
    ),
    #
    # altri gram negativi
    _instruction(
        "respiratorio",
        "Respiratorio (BAL+BAS+ESP)",
        "acibcx",
        "Acinetobacter baumannii complex",
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "pseaer", "Pseudomonas aeruginosa"
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "psespp", "Pseudomonas spp"
    ),
    _instruction(
        "respiratorio",
        "Respiratorio (BAL+BAS+ESP)",
        "psemal",
        "Stenotrophomonas maltophilia",
    ),
    #
    # altri batteri
    #
    # Gram positivi
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "entspp", "Enterococcus spp"
    ),
    _instruction(
        "respiratorio", "Respiratorio (BAL+BAS+ESP)", "staaur", "Staphylococcus aureus"
    ),
    #
    # altri batteri
    #
    # micobatteri
    #
    # funghi
    #
    # virus
]


instructions = (
    sorv_pass_instructions
    + sangue_liquor_instructions
    + liquor_instructions
    + sangue_instructions
    + urine_instructions
    + urine_cv_instructions
    + respiratorio_instructions
)

rate_instructions = [
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "acibcx",
        "A. baumannii (MDR)",
        select_fn=lambda df: df.resistente.str.split("|").map(
            lambda x: "MDR" in x, na_action="ignore"
        ),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "clodif",
        "C. difficile",
        select_fn=lambda df: df.resistente.map(lambda x: True),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "entspp",
        "Enterococcus spp (VRE)",
        select_fn=lambda df: df.resistente.str.split("|").map(
            lambda x: "VRE" in x, na_action="ignore"
        ),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "esccol",
        "E. coli (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "klepne",
        "K. pneumoniae (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "klepne",
        "K. pneumoniae (MDR)",
        select_fn=lambda df: df.resistente.str.split("|").map(
            lambda x: "MDR" in x, na_action="ignore"
        ),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "pseaer",
        "Pseudomonas aeruginosa (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "sermar",
        "S. marcescens",
        select_fn=lambda df: df.resistente.map(lambda x: True),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        "staaur",
        "MRSA",
        select_fn=lambda df: df.resistente.str.split("|").map(
            lambda x: "OXA" in x, na_action="ignore"
        ),
    ),
    _rate_instruction(
        "sorv_pass",
        "Sorveglianza passiva (noPS, noMAC)",
        ["prospp", "kleoxy", "klespp", "citspp", "psespp"],
        "Altri MDRO (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
    _rate_instruction(
        "sangue",
        "Sangue (noPS, noMAC)",
        [
            "acibcx",
            "entspp",
            "esccol",
            "kleoxy",
            "klespp",
            "klepne",
            "prospp",
            "pseaer",
            "psespp",
            "staaur",
        ],
        "Batteriemie da MDRO (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
    _rate_instruction(
        "urine",
        "Urine (tutte, noPS, noMAC)",
        [
            "acibcx",
            "entspp",
            "esccol",
            "kleoxy",
            "klespp",
            "klepne",
            "prospp",
            "pseaer",
            "psespp",
            "staaur",
        ],
        "UTI da MDRO (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
    _rate_instruction(
        "urine_cv",
        "Urine (CV, noPS, noMAC)",
        [
            "acibcx",
            "entspp",
            "esccol",
            "kleoxy",
            "klespp",
            "klepne",
            "prospp",
            "pseaer",
            "psespp",
            "staaur",
        ],
        "CAUTI da MDRO (qualunque resistenza)",
        select_fn=lambda df: df.resistente.astype(bool),
    ),
]
