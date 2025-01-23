def calculate_stock_score(cagr, beta, pe_ratio, eps, dividend_yield,for_radar=False):
    try:
        try:
            cagr = float(cagr.replace('%', ''))
        except ValueError as e:
            print(f"Erreur de conversion du CAGR : {e}")
            return 0.0
        
        try:
            beta = float(beta)
        except ValueError:
            beta = 1.0

        try:
            pe_ratio = float(pe_ratio)
        except ValueError:
            pe_ratio = 30.0

        try:
            eps = float(eps)
        except ValueError:
            eps = 5.0
            
        dividend_yield = 0.0 if dividend_yield == "None" else float(dividend_yield)
    except ValueError as e:
        print(f"Erreur de conversion des valeurs numériques : {e}")
        return None

    # Pondérations
    weights = {
        "cagr": 0.2,             # Importance élevée pour la croissance
        "beta": 0.2,             # Importance modérée pour la stabilité
        "pe_ratio": 0.2,         # Importance modérée pour la valorisation
        "eps": 0.2,              # Importance modérée pour la rentabilité
        "dividend_yield": 0.2,   # Faible importance pour les dividendes
    }

    # Calcul des scores individuels
    cagr_score = calculate_cagr_score(cagr)
    beta_score = calculate_beta_score(beta)
    pe_score = calculate_pe_ratio_score(pe_ratio)
    eps_score = calculate_eps_score(eps)
    dividend_yield_score = calculate_dividend_yield_score(dividend_yield)

    # Score total pondéré
    total_score = (
        cagr_score * weights["cagr"] +
        beta_score * weights["beta"] +
        pe_score * weights["pe_ratio"] +
        eps_score * weights["eps"] +
        dividend_yield_score * weights["dividend_yield"]
    )

    if for_radar:
        return [{"criteria": "CAGR", "score": cagr_score, "out of": 1.0},
                {"criteria": "Beta", "score": beta_score, "out of": 1.0},
                {"criteria": "P/E Ratio", "score": pe_score, "out of": 1.0},
                {"criteria": "EPS", "score": eps_score, "out of": 1.0},
                {"criteria": "Dividend Yield", "score": dividend_yield_score, "out of": 1.0}]
    else:
        return round(total_score * 10, 2)

# Fonctions de calcul des scores individuels
def calculate_dividend_yield_score(dividend_yield):
    if dividend_yield < 0.01:
        return 1.0
    elif 0.01 <= dividend_yield <= 0.03:
        return 0.5 - 0.5 * (dividend_yield - 0.01) / 0.01
    else:
        return 0.0

def calculate_eps_score(eps):
    if eps > 15:
        return 1.0
    elif 10 <= eps <= 15:
        return 0.75 + 0.25 * (eps - 10) / 5
    elif 5 <= eps < 10:
        return 0.5 + 0.25 * (eps - 5) / 5
    elif 1 <= eps < 5:
        return 0.25 * (eps - 1) / 4
    else:
        return 0.0

def calculate_pe_ratio_score(pe_ratio):
    if pe_ratio > 30:
        return 0.5
    elif 15 <= pe_ratio <= 30:
        return 1.0
    elif 0 <= pe_ratio < 15:
        return 0.5 * pe_ratio / 15
    else:
        return 0.0

def calculate_beta_score(beta):
    if beta > 2:
        return 1.0
    elif 1 <= beta <= 2:
        return 0.75 + 0.25 * (beta - 1) / 1
    elif 0.75 <= beta < 1:
        return 0.25 + 0.25 * (beta - 0.75) / 0.25
    else:
        return 0.25

def calculate_cagr_score(cagr):
    if cagr > 15:
        return 1.0
    elif 5 <= cagr <= 15:
        return 0.67 + 0.33 * (cagr - 5) / 5
    elif 0 <= cagr < 5:
        return 0.33 * cagr / 5
    else:
        return 0.0
