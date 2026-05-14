from app.controller.compute_controller import compute_conditional, compute_total, compute_bayes
from app.common.logger import error
from app.common.utils import safe_float, get_n_floats, print_formula_result

def main_menu():
    print("========== Probable Computing Machine ==========")
    print("Choose calculation type:")
    print("1. Conditional Probability  (P(A|B) = P(A∩B)/P(B))")
    print("2. Total Probability        (P(A) = Σ P(Bi) * P(A|Bi))")
    print("3. Bayes' Theorem           (P(A|B) = P(B|A) * P(A) / P(B))")
    print("===============================================")
    return input("Please enter your choice (1/2/3): ").strip()

def main():
    try:
        choice = main_menu()
        if choice == "1":
            p_ab = safe_float("Enter P(A ∩ B): ")
            p_b = safe_float("Enter P(B): ")
            result = compute_conditional(p_ab, p_b)
            print_formula_result(result.msg, result.value, None if result.code == 0 else result.msg)
        elif choice == "2":
            n = int(safe_float("Number of events Bi: "))
            p_bi = get_n_floats(n, "P(Bi)")
            p_abi = get_n_floats(n, "P(A|Bi)")
            result = compute_total(p_bi, p_abi)
            print_formula_result(result.msg, result.value, None if result.code == 0 else result.msg)
        elif choice == "3":
            p_b_given_a = safe_float("Enter P(B|A): ")
            p_a = safe_float("Enter P(A): ")
            p_b = safe_float("Enter P(B): ")
            result = compute_bayes(p_b_given_a, p_a, p_b)
            print_formula_result(result.msg, result.value, None if result.code == 0 else result.msg)
        else:
            print("Invalid selection.")
    except Exception as ex:
        error(str(ex))

if __name__ == "__main__":
    main()
