atm_vault_balance = 50_000_000
user_account_balance = 10_000_000


def display_balances():
    """
    Display the current account balance and ATM vault balance.

    Reads both global variables and prints them to the screen.
    The vault balance is printed for debug purposes only.

    Parameters: None.
    Returns: None.
    """
    print("--- SỐ DƯ TÀI KHOẢN ---")
    print(f"Tài khoản của bạn: {user_account_balance:,.0f} VND".replace(",", "."))
    print(f"(Debug) Tiền mặt trong ATM: {atm_vault_balance:,.0f} VND".replace(",", "."))


def deposit_money(amount):
    """
    Deposit money into the user's account and the ATM vault.

    Both global balances increase by the given amount because
    physical cash is inserted into the machine.

    Parameters:
        amount (int): Amount of money to deposit. Must be greater than 0.

    Returns:
        bool: True if the deposit was successful.
    """
    global user_account_balance, atm_vault_balance
    user_account_balance += amount
    atm_vault_balance += amount
    formatted = f"{user_account_balance:,.0f}".replace(",", ".")
    print(f"Giao dịch thành công! Số dư tài khoản hiện tại: {formatted} VND.")
    return True


def check_withdrawal_rules(amount):
    """
    Validate a withdrawal request against business rules.

    Calculates the transaction fee and total deduction, then checks
    three conditions: multiple-of-50000, sufficient user funds,
    and sufficient ATM cash.

    Parameters:
        amount (int): Amount the user wants to withdraw. Must be > 0
                      and a multiple of 50,000.

    Returns:
        str: One of three status codes:
             "NOT_MULTIPLE"        — amount is not a multiple of 50,000
             "INSUFFICIENT_FUNDS"  — user account cannot cover amount + fee
             "ATM_OUT_OF_CASH"     — ATM vault has less cash than amount
             "OK"                  — all conditions passed
    """
    fee = 1100
    total_deduction = amount + fee

    if amount % 50_000 != 0:
        return "NOT_MULTIPLE"
    if total_deduction > user_account_balance:
        return "INSUFFICIENT_FUNDS"
    if amount > atm_vault_balance:
        return "ATM_OUT_OF_CASH"
    return "OK"


def execute_withdrawal(total_deduction, amount_to_dispense):
    """
    Execute the withdrawal by updating both global balances and printing a receipt.

    Called only after check_withdrawal_rules() returns "OK".
    Deducts total_deduction (amount + fee) from the user account,
    and deducts amount_to_dispense (cash given out) from the ATM vault.

    Parameters:
        total_deduction   (int): Amount deducted from user account (amount + fee).
        amount_to_dispense(int): Actual cash dispensed from the ATM vault.

    Returns: None.
    """
    global user_account_balance, atm_vault_balance
    fee = total_deduction - amount_to_dispense
    user_account_balance -= total_deduction
    atm_vault_balance -= amount_to_dispense

    formatted_amount  = f"{amount_to_dispense:,.0f}".replace(",", ".")
    formatted_fee     = f"{fee:,.0f}".replace(",", ".")
    formatted_balance = f"{user_account_balance:,.0f}".replace(",", ".")

    print("Giao dịch đang xử lý...")
    print(f"Phí giao dịch: {formatted_fee} VND")
    print(f"Bạn đã rút thành công {formatted_amount} VND.")
    print(f"Số dư tài khoản còn lại: {formatted_balance} VND.")


def main():
    """
    Run the main ATM loop, displaying the menu and routing user choices
    to the appropriate handler functions.

    Parameters: None.
    Returns: None.
    """
    while True:
        print("\n============= SMART ATM =============")
        print("1. Xem số dư")
        print("2. Nạp tiền")
        print("3. Rút tiền")
        print("4. Kết thúc giao dịch")
        print("=====================================")
        choice = input("Vui lòng chọn giao dịch (1-4): ").strip()

        match choice:
            case "1":
                display_balances()

            case "2":
                print("--- NẠP TIỀN ---")
                raw = input("Nhập số tiền muốn nạp: ").strip()
                if not raw.isdigit():
                    print("Số tiền không hợp lệ.")
                    continue
                amount = int(raw)
                if amount <= 0:
                    print("Số tiền không hợp lệ.")
                    continue
                deposit_money(amount)

            case "3":
                print("--- RÚT TIỀN ---")
                raw = input("Nhập số tiền cần rút: ").strip()
                if not raw.isdigit():
                    print("Số tiền không hợp lệ.")
                    continue
                amount = int(raw)
                if amount <= 0:
                    print("Số tiền không hợp lệ.")
                    continue
                status = check_withdrawal_rules(amount)
                match status:
                    case "NOT_MULTIPLE":
                        print("Số tiền rút phải là bội số của 50,000.")
                    case "INSUFFICIENT_FUNDS":
                        print("Giao dịch thất bại: Số dư tài khoản không đủ.")
                    case "ATM_OUT_OF_CASH":
                        print("Giao dịch thất bại: Máy ATM không đủ tiền mặt để phục vụ.")
                    case "OK":
                        fee = 1100
                        execute_withdrawal(amount + fee, amount)

            case "4":
                print("Cảm ơn quý khách đã sử dụng dịch vụ!")
                break

            case _:
                print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 4.")


main()
