"""
Global Variables
atm_vault_balance = 50000000
user_account_balance = 10000000

Hai biến này đại diện cho trạng thái chung của hệ thống ATM nên được khai báo toàn cục.

Hàm sử dụng Arguments
deposit_money(amount) → nhận số tiền cần nạp.
check_withdrawal_rules(amount) → nhận số tiền muốn rút.
execute_withdrawal(total_deduction, amount_to_dispense) → nhận tổng tiền cần trừ và số tiền thực tế trả ra.
Hàm thao tác trực tiếp với Global Variables
display_balances()
deposit_money()
execute_withdrawal()

Các hàm này cần cập nhật hoặc đọc trực tiếp trạng thái hệ thống nên sử dụng global.

Luồng rút tiền
Người dùng nhập số tiền.
Gọi check_withdrawal_rules(amount).
Hàm trả về:
"INVALID_AMOUNT"
"INVALID_MULTIPLE"
"INSUFFICIENT_FUNDS"
"ATM_OUT_OF_CASH"
"OK"
Nếu "OK" → gọi execute_withdrawal().
"""

atm_vault_balance = 50000000
user_account_balance = 10000000


def display_balances():
    print("\n--- SỐ DƯ TÀI KHOẢN ---")
    print(f"Tài khoản của bạn: {user_account_balance:,} VND")
    print(f"(Debug) Tiền mặt trong ATM: {atm_vault_balance:,} VND")


def deposit_money(amount):
    global user_account_balance
    global atm_vault_balance

    user_account_balance += amount
    atm_vault_balance += amount

    return True


def check_withdrawal_rules(amount):
    fee = 1100
    total_deduction = amount + fee

    if amount <= 0:
        return "INVALID_AMOUNT", 0, 0

    if amount % 50000 != 0:
        return "INVALID_MULTIPLE", 0, 0

    if total_deduction > user_account_balance:
        return "INSUFFICIENT_FUNDS", 0, fee

    if amount > atm_vault_balance:
        return "ATM_OUT_OF_CASH", 0, fee

    return "OK", total_deduction, fee


def execute_withdrawal(total_deduction, amount_to_dispense):
    global user_account_balance
    global atm_vault_balance

    user_account_balance -= total_deduction
    atm_vault_balance -= amount_to_dispense

    print("Giao dịch đang xử lý...")
    print("Phí giao dịch: 1,100 VND")
    print(f"Bạn đã rút thành công {amount_to_dispense:,} VND.")
    print(
        f"Số dư tài khoản còn lại: {user_account_balance:,} VND."
    )


def show_menu():
    print("\n============= SMART ATM =============")
    print("1. Xem số dư")
    print("2. Nạp tiền")
    print("3. Rút tiền")
    print("4. Kết thúc giao dịch")
    print("=====================================")


def main():
    while True:
        show_menu()

        choice = input("Vui lòng chọn giao dịch (1-4): ")

        if choice == "1":
            display_balances()

        elif choice == "2":
            print("\n--- NẠP TIỀN ---")

            amount = int(input("Nhập số tiền muốn nạp: "))

            if amount <= 0:
                print("Số tiền không hợp lệ")
                continue

            if deposit_money(amount):
                print(
                    f"Giao dịch thành công! "
                    f"Số dư tài khoản hiện tại: "
                    f"{user_account_balance:,} VND."
                )

        elif choice == "3":
            print("\n--- RÚT TIỀN ---")

            amount = int(input("Nhập số tiền cần rút: "))

            status, total_deduction, fee = check_withdrawal_rules(amount)

            if status == "INVALID_AMOUNT":
                print("Số tiền không hợp lệ")

            elif status == "INVALID_MULTIPLE":
                print("Số tiền rút phải là bội số của 50,000")

            elif status == "INSUFFICIENT_FUNDS":
                print(
                    "Giao dịch thất bại: "
                    "Số dư tài khoản không đủ."
                )

            elif status == "ATM_OUT_OF_CASH":
                print(
                    "Giao dịch thất bại: "
                    "Máy ATM không đủ tiền mặt để phục vụ."
                )

            elif status == "OK":
                execute_withdrawal(
                    total_deduction,
                    amount
                )

        elif choice == "4":
            print("Cảm ơn quý khách đã sử dụng dịch vụ!")
            break

        else:
            print("Lựa chọn không hợp lệ.")


main()