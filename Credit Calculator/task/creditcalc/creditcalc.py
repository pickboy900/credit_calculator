# write your code here
from math import ceil, log, floor
from argparse import ArgumentParser, ArgumentTypeError
from sys import argv as args
import re
from collections import namedtuple

# add parsed arguments
parser = ArgumentParser()


# define invalid parameter combination
# cmd = None
# annuity_payment = 0
# monthly_payment = 0
# principal = 0
# number_of_period = 0
# credit_interest = 0
# if cmd == "p":
#     annuity_payment = float(input("Enter the annuity payment:\n"))
# else:
#     principal = float(input("Enter the credit principal:\n"))
# if cmd == "n":
#     monthly_payment = float(input("Enter the monthly payment:\n"))
# else:
#     number_of_period = float(input("Enter the number of periods:\n"))
# credit_interest = float(input("Enter the credit interest:\n"))
#
# i = credit_interest / (12*100)
# # print(cmd)
# if cmd == "n":
#     n = math.ceil(math.log((monthly_payment / (monthly_payment-(i * principal))), (1+i)))
#     year = n // 12
#     month = n % 12
#     output = "It will take "
#     if year:
#         output += f'{year} year{"s" if year > 1 else ""} and '
#     if month:
#         output += f'{month} month{"s" if month > 1 else ""}'
#     output += " to repay this credit!"
#     print(output)
# else:
#     n = number_of_period
#
# if cmd == "p":
#     p = annuity_payment / ((i * (1+i)**n) / ((i+1)**n - 1))
#     print(f'Your credit principal = {round(p)}!')
#
# if cmd == "a":
#     a = principal * ((i*(i+1)**n) / ((i+1)**n - 1))
#     print(f"Your monthly payment = {math.ceil(a)}!")


def calculate_n(annuity_payment: float, principal: float, interest: float):
    """
    calculate number of periods or months to pay credit principal
    """
    return ceil(log((annuity_payment / (annuity_payment - (interest * principal))), (1 + interest)))


def calculate_and_show_time(periods: int):
    year = periods // 12
    month = periods % 12
    output = "It will take "
    if year:
        output += f'{year} year{"s" if year > 1 else ""} '
    if month:
        output += f'and {month} month{"s" if month > 1 else ""} '
    output += "to repay this credit!"
    print(output)


def calculate_p(annuity_payment: float, periods: int, interest: float):
    return annuity_payment / ((interest * (1 + i) ** periods) / ((interest + 1) ** periods - 1))


def calculate_a(p: float, interest: float, periods: int):
    return p * ((interest * (interest + 1) ** periods) / ((interest + 1) ** periods - 1))


def calculate_d(principal: float, periods: int, m: int, interest: float):
    return (principal / periods) + (interest * (principal - ((principal * (m - 1)) / periods)))
    pass


# restrict any negative value
def non_negative_float(string: str):
    """
    restrict any negative value
    """
    value = float(string)
    if value > -1:
        return value
    raise ArgumentTypeError("Incorrect parameters")


def non_negative_int(string: str):
    """
    restrict any negative value
    """
    value = int(string)
    if value > -1:
        return value
    raise ArgumentTypeError("Incorrect parameters")


if __name__ == '__main__':
    # if arguments count is less than 4 the error
    if len(args) < 5:
        print("Incorrect parameters")
    else:
        # design a namespace namedtuple
        keys = [re.findall(r'--(\w+)=', arg)[0] for arg in args[1:]]
        values = [re.findall(r'=(.+)', arg)[0] for arg in args[1:]]
        required_fields = {'type', 'interest'}
        dict_parameter: dict = dict(zip(keys, values))
        all_good = True
        if not set(keys).intersection(required_fields) == required_fields:
            # --payment with --type=diff is invalid
            all_good = False
        else:
            # any negative parameter value is restricted
            for field in keys[1:]:
                try:
                    if not float(dict_parameter[field]) > -1:
                        all_good = False
                except ValueError:
                    all_good = False
                    break
        if all_good:
            print("all required met")
            Parser = namedtuple('Parser', keys)
            values = values[:1] + list(map(float, values[1:]))
            parsed_args = Parser(*values)
            i = parsed_args.interest / (12 * 100)
            if 'periods' not in dict_parameter:
                n = calculate_n(annuity_payment=parsed_args.payment, principal=parsed_args.principal, interest=i)
                # calculate_and_show_time(n)
            else:
                n = int(parsed_args.periods)
            if parsed_args.type == 'diff':
                credit_principal = parsed_args.principal
                total = sum(
                    ceil(calculate_d(principal=credit_principal, m=m + 1, interest=i, periods=n)) \
                    for m in range(n))
                for m in range(n):
                    print(f'Month {m + 1}: payment is '
                          f'{ceil(calculate_d(principal=parsed_args.principal, m=m + 1, interest=i, periods=n))}')
                print("\n")
                print(f'Overpayment = {round(total - credit_principal)}')
            else:
                # confirm that annuity payment is defined
                if 'payment' not in dict_parameter:
                    payment = ceil(calculate_a(parsed_args.principal, i, n))
                    print(f'Your annuity payment = {payment}!')
                else:
                    payment = parsed_args.payment
                # confirm credit principal
                if 'principal' in dict_parameter.keys():
                    credit_principal = parsed_args.principal
                else:
                    credit_principal = calculate_p(payment, n, i)
                total = payment * n
                if 'payment' in dict_parameter.keys():
                    print(f'Your credit principal = {floor(credit_principal)}!')
                if 'periods' not in dict_parameter.keys():
                    calculate_and_show_time(n)
                print(f'Overpayment = {ceil(total - credit_principal)}')
        else:
            print("Incorrect parameters")


        # # --payment with --type=diff is invalid
        # parser.add_argument('--type', required=True, choices=['annuity', 'diff'])
        # # interest is required cause it can't calculate it
        # parser.add_argument('--interest', required=True)
        # parser.add_argument('--periods')
        # parser.add_argument('--principal')
        #
        # parser.add_argument('--payment', type=non_negative_float)
        # parsed_args = parser.parse_args()
