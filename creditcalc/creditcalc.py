import argparse
from math import ceil, log, floor, pow


class InvalidArgument(Exception):
    pass


TYPE_M_FOR_NUMBER_OF_MONTHLY_PAYMENTS = 'type "m" for number of monthly payments'
TYPE_P_FOR_MONTHLY_PAYMENT_AMOUNT = 'type "p" for the monthly payment:'

WHAT_DO_YOU_WANT_TO_CALCULATE = 'What do you want to calculate?'
NUMBER_OF_MONTHLY_PAYMENTS = 'type "n" for number of monthly payments,'
ANNUITY_MONTHLY_PAYMENT_AMOUNT = 'type "a" for annuity monthly payment amount,'

LOAN_PRINCIPAL = 'type "p" for loan principal:'
TYPE_ANNUITY_MONTHLY_PAYMENT_AMOUNT = 'type "a" for annuity monthly payment amount,'
TYPE_LOAN_PRINCIPAL = 'type "p" for loan principal:'
IT_WILL_TAKE_MONTHS_TO_REPAY_THIS_LOAN = 'It will take %d years and %d months to repay this loan!'
YOUR_MONTHLY_PAYMENT = 'Your annuity payment = %d!'
YOUR_LOAN_PRINCIPAL = 'Your loan principal = %d!'
MONTH_PAYMENT_IS = 'Month %d: payment is %d'
OVERPAYMENT = 'Overpayment = %d'
INCORRECT_PARAMETERS = 'Incorrect parameters'


def convert_months_to_years(months):
    return [floor(months / 12), months % 12]


def calculate_nominal_interest_rate(loan_interest_arg):
    return loan_interest_arg / 1200


def calculate_loan_interest_part(nominal_interest_rate_arg, nr_of_months_arg):
    return pow((1 + nominal_interest_rate_arg), nr_of_months_arg)


def calculate_monthly_payment(loan_principal_arg, nr_of_monthly_payments_arg, loan_interest_arg):
    nominal_interest_rate = calculate_nominal_interest_rate(loan_interest_arg)
    loan_interest_part = calculate_loan_interest_part(nominal_interest_rate, nr_of_monthly_payments_arg)
    return ceil(loan_principal_arg * (nominal_interest_rate * loan_interest_part) / (loan_interest_part - 1))


def calculate_number_of_monthly_payments(loan_principal_arg, monthly_payment_arg, loan_interest_arg):
    nir = calculate_nominal_interest_rate(loan_interest_arg)
    return ceil(log(
        monthly_payment_arg / (monthly_payment_arg - nir * loan_principal_arg),
        1 + nir
    ))


def calculate_loan_principal(monthly_payment_arg, nr_of_months_arg, loan_interest_arg):
    nominal_interest_rate = calculate_nominal_interest_rate(loan_interest_arg)
    loan_interest_part = calculate_loan_interest_part(nominal_interest_rate, nr_of_months_arg)
    return monthly_payment_arg / (nominal_interest_rate * loan_interest_part / (loan_interest_part - 1))


def calculate_differentiated_payment_month(
        principal_arg,
        nominal_interest_rate_arg,
        months_arg,
        current_month_arg
):
    sub_equation = principal_arg * (current_month_arg - 1) / months_arg
    return ceil((principal_arg / months_arg) + nominal_interest_rate_arg * (principal_arg - sub_equation))


def process_number_of_monthly_payments():
    nr_of_monthly_payments = calculate_number_of_monthly_payments(args.principal, args.payment,
                                                                  args.interest)
    [years, months] = convert_months_to_years(nr_of_monthly_payments)
    print(IT_WILL_TAKE_MONTHS_TO_REPAY_THIS_LOAN % (years, months))
    print(OVERPAYMENT % (args.payment * nr_of_monthly_payments - args.principal))


def process_annuity_monthly_payment_amount():
    your_monthly_payment = calculate_monthly_payment(args.principal, args.periods, args.interest)
    print(YOUR_MONTHLY_PAYMENT % your_monthly_payment)
    print(OVERPAYMENT % (your_monthly_payment * args.periods - args.principal))


def process_loan_principal():
    loan_principal = calculate_loan_principal(args.payment, args.periods, args.interest)
    print(YOUR_LOAN_PRINCIPAL % loan_principal)


def process_loan_diff():
    nominal_interest_rate = calculate_nominal_interest_rate(args.interest)
    amounts = [
        calculate_differentiated_payment_month(
            principal_arg=args.principal,
            months_arg=args.periods,
            current_month_arg=current_month_index + 1,
            nominal_interest_rate_arg=nominal_interest_rate
        )
        for current_month_index in range(0, args.periods)
    ]

    for current_month_index, amount in enumerate(amounts):
        print(MONTH_PAYMENT_IS % (current_month_index + 1, amount))

    print(OVERPAYMENT % (sum(amounts) - args.principal))


ACTIONS = {
    "annuity": {
        "n": process_number_of_monthly_payments,
        "a": process_annuity_monthly_payment_amount,
        "p": process_loan_principal,
    },
    "diff": {
        "d": process_loan_diff
    }
}

ACTION_RESOLVERS = {
    "annuity": {
        "n": lambda args_arg:
        args_arg.principal is not None
        and args_arg.payment is not None
        and args_arg.interest is not None
        and args_arg.periods is None,

        "a": lambda args_arg:
        args_arg.principal is not None
        and args_arg.periods is not None
        and args_arg.interest is not None
        and args_arg.payment is None,

        "p": lambda args_arg:
        args_arg.payment is not None
        and args_arg.periods is not None
        and args_arg.interest is not None
        and args_arg.principal is None,
    },
    "diff": {
        'd': lambda args_arg:
        args_arg.payment is None
        and args_arg.principal is not None
        and args_arg.periods is not None
        and args_arg.interest is not None,
    }
}

parser = argparse.ArgumentParser()
parser.add_argument('--type', choices=['annuity', 'diff'])
parser.add_argument('--payment', type=int)
parser.add_argument('--principal', type=int)
parser.add_argument('--periods', type=int)
parser.add_argument('--interest', type=float, help='Incorrect parameters')

PARSER_EXAMPLES = {
    "annuity": {
        # "n": lambda: parser.parse_args(['--type=annuity', '--principal=10000', '--payment=10', '--interest=12']),
        "n": lambda: parser.parse_args(['--type=annuity', '--principal=500000', '--payment=23000', '--interest=7.8']),
        "a": lambda: parser.parse_args(['--type=annuity', '--principal=10000', '--periods=10', '--interest=12']),
        "p": lambda: parser.parse_args(['--type=annuity', '--payment=10000', '--periods=10', '--interest=12']),
    },
    "diff": {
        'd': lambda: parser.parse_args(['--type=diff', '--principal=1000000', '--periods=10', '--interest=10'])
    }
}

# args = PARSER_EXAMPLES['diff']['d']()
args = parser.parse_args()


def resolve_action():
    resolved_action = [action for action, is_action in ACTION_RESOLVERS[args.type].items() if is_action(args)]
    if len(resolved_action) < 1:
        raise InvalidArgument
    return resolved_action[0]


try:
    ACTIONS[args.type][resolve_action()[0]]()
except InvalidArgument:
    print(INCORRECT_PARAMETERS)
