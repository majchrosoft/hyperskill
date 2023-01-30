class ExitFlowException(Exception):
    pass


class GoToMainMenuFlowException(Exception):
    pass


MSG_STARTING_TO_MAKE_A_COFFEE = 'Starting to make a coffee'
MSG_GRINDING_COFFEE_BEANS = 'Grinding coffee beans'
MSG_BOILING_WATER = 'Boiling water'
MSG_MIXING_BOILED_WATER_WITH_CRUSHED_COFFEE_BEANS = 'Mixing boiled water with crushed coffee beans'
MSG_POURING_COFFEE_INTO_THE_CUP = 'Pouring coffee into the cup'
MSG_POURING_SOME_MILK_INTO_THE_CUP = 'Pouring some milk into the cup!'
MSG_COFFEE_IS_READY = 'Coffee is ready!'

MSG_WRITE_HOW_MANY_CUPS_OF_COFFEE_YOU_WILL_NEED = 'Write how many cups of coffee you will need:'
MSG_FOR_CUPS_OF_COFFEE_YOU_WILL_NEED = 'For %s cups of coffee you will need:'
MSG_ML_OF = '%d %s of %s'
MSG_WRITE_HOW_MANY_OF_THE_COFFEE_MACHINE_HAS = 'Write how many %s of %s the coffee machine has:'
MSG_YES_I_CAN_MAKE_THAT_AMOUNT_OF_COFFEE = 'Yes, I can make that amount of coffee'
MSG_NO_I_CAN_MAKE_ONLY_CUPS_OF_COFFEE = 'No, I can make only %s cups of coffee'
MSG_AND_MORE = ' (and even %d more than that)'
MSG_WRITE_ACTION = 'Write action (%s): '
MSG_WHAT_DO_YOU_WANT_TO_BUY = 'What do you want to buy? %s, back - to main menu'
MSG_CUPS = '%d %sdisposable %ss'
MSG_MONEY = '$%d of money'
MSG_I_GAVE_YOU = 'I gave you $%d'
MSG_SORRY_NOT_ENOUGH = 'Sorry, not enough %s!'
MSG_I_HAVE_ENOUGH_RESOURCES = 'I have enough resources, making you a coffee!'

MSG_FILL_WATER = 'Write how many ml of water you want to add:'
MSG_FILL_MILK = 'Write how many ml of milk you want to add:'
MSG_FILL_BEANS = 'Write how many grams of coffee beans you want to add:'
MSG_FILL_CUPS = 'Write how many disposable cups you want to add:'
MSGS_FILL = MSG_FILL_WATER, MSG_FILL_MILK, MSG_FILL_BEANS, MSG_FILL_CUPS,

INGREDIENT_WATER, INGREDIENT_MILK, INGREDIENT_BEAN, INGREDIENT_CUP = 'water', 'milk', 'coffee beans', 'cup'
INGREDIENTS = INGREDIENT_WATER, INGREDIENT_MILK, INGREDIENT_BEAN, INGREDIENT_CUP

UNIT_ML, UNIT_GRAM, UNIT_CUP = 'ml', 'g', ''
UNITS = UNIT_ML, UNIT_GRAM
INGREDIENTS_UNITS = UNIT_ML, UNIT_ML, UNIT_GRAM, UNIT_CUP

COFFEE_ESPRESSO, COFFEE_LATTE, COFFEE_CAPPUCCINO = 'espresso', 'latte', 'cappuccino'
COFFEES = COFFEE_ESPRESSO, COFFEE_LATTE, COFFEE_CAPPUCCINO

COFFEE_INGREDIENTS_ESPRESSO = 250, 0, 16, 1
COFFEE_INGREDIENTS_LATTE = 350, 75, 20, 1,
COFFEE_INGREDIENTS_CAPPUCCINO = 200, 100, 12, 1
COFFEE_INGREDIENTS = COFFEE_INGREDIENTS_ESPRESSO, COFFEE_INGREDIENTS_LATTE, COFFEE_INGREDIENTS_CAPPUCCINO

WATER, MILK, COFFEE_BEANS, CUPS = 'water', 'milk', 'coffee beans', 'cups'
COFFEE_INGREDIENT_NAMES = WATER, MILK, COFFEE_BEANS, CUPS

MSGS_COFFEE_INGREDIENTS = MSG_ML_OF, MSG_ML_OF, MSG_ML_OF, MSG_CUPS

COFFEE_COSTS = 4, 7, 6

ACTION_BUY, ACTION_FILL, ACTION_TAKE, ACTION_REMAINING, ACTION_EXIT = "buy", "fill", "take", "remaining", "exit"
ACTIONS = ACTION_BUY, ACTION_FILL, ACTION_TAKE, ACTION_REMAINING, ACTION_EXIT

RESOURCES = [400, 540, 120, 9]
BANK = 550


def ask_question_open(message_arg, cast_to_arg=int):
    message_arg and print(message_arg)
    return cast_to_arg(input())


def ask_question_closed(message_arg, possible_answers_arg, cast_to, message_fail_arg='',
                        message_fail_extended_arg=None):
    while True:
        try:
            message_arg and print(message_arg)

            user_input = input()
            if user_input == 'back':
                raise GoToMainMenuFlowException

            answer = cast_to(user_input)
        except ValueError:
            message_fail_arg and print(message_fail_arg)
            return ask_question_closed(message_arg, possible_answers_arg, cast_to, message_fail_arg,
                                       message_fail_extended_arg)

        if answer in possible_answers_arg:
            break
        message_fail_extended_arg is not None and message_fail_extended_arg(answer, possible_answers_arg)
        message_fail_arg and print(message_fail_arg)
    return answer


def calculate_ingredients(coffee_cups, coffee):
    return [ingredient_ml * coffee_cups for ingredient_ml in COFFEE_INGREDIENTS[coffee]]


def coffee_buy(coffee_cups, coffee):
    global RESOURCES, BANK
    coffee_ingredients = calculate_ingredients(coffee_cups, coffee)

    if coffees_count(RESOURCES, coffee) <= 0:
        show_message_not_enough(RESOURCES, coffee)
        return

    print(MSG_I_HAVE_ENOUGH_RESOURCES)
    RESOURCES = [ingredient_count - coffee_ingredients[index] for index, ingredient_count in
                 enumerate(RESOURCES)]
    BANK += COFFEE_COSTS[coffee]


def show_resources(resources_arg, money):
    print('\n'.join([MSGS_COFFEE_INGREDIENTS[index] % (ingredient_ml, INGREDIENTS_UNITS[index], INGREDIENTS[index]) for
                     index, ingredient_ml in
                     enumerate(resources_arg)]))
    print(MSG_MONEY % money)


def serve_ingredients_pick():
    return [ask_question_open(MSG_WRITE_HOW_MANY_OF_THE_COFFEE_MACHINE_HAS % (INGREDIENTS_UNITS[index], ingredient)) for
            index, ingredient in enumerate(INGREDIENTS)]


def ingredients_pick(messages):
    return [ask_question_open(messages[index]) for
            index, ingredient in enumerate(INGREDIENTS)]


def serve_resolve_how_many_coffees(coffees_desired, coffees_in_store):
    msgs = (MSG_YES_I_CAN_MAKE_THAT_AMOUNT_OF_COFFEE,
            MSG_YES_I_CAN_MAKE_THAT_AMOUNT_OF_COFFEE + MSG_AND_MORE % (coffees_in_store - coffees_desired),
            MSG_NO_I_CAN_MAKE_ONLY_CUPS_OF_COFFEE % coffees_in_store)
    msg_resolvers = (
        coffees_desired == coffees_in_store,
        coffees_desired < coffees_in_store,
        coffees_desired > coffees_in_store,
    )
    return [msg for index, msg in enumerate(msgs) if msg_resolvers[index]][0]


def coffees_count(resources, coffee):
    return min(
        [units // COFFEE_INGREDIENTS[coffee][index] if COFFEE_INGREDIENTS[coffee][index] > 0 else units for index, units
         in enumerate(resources)])


def show_message_not_enough(resources, coffee):
    print(''.join([MSG_SORRY_NOT_ENOUGH % COFFEE_INGREDIENT_NAMES[index] for index, units in enumerate(resources) if
                   units - COFFEE_INGREDIENTS[coffee][index] < 0]))


def serve_buy():
    coffee = ask_question_closed(
        MSG_WHAT_DO_YOU_WANT_TO_BUY % ', '.join(
            [str(index + 1) + ' ' + coffee for index, coffee in enumerate(COFFEES)]),
        [index + 1 for index, coffee in enumerate(COFFEES)],
        int
    ) - 1
    coffee_buy(1, coffee)


def serve_fill():
    global RESOURCES, BANK
    fill = ingredients_pick(MSGS_FILL)
    RESOURCES = [ingredients + fill[index] for index, ingredients in
                 enumerate(RESOURCES)]


def serve_take():
    global BANK
    # to_be_taken = BANK - money if BANK - money else 0
    # to_be_taken = BANK
    to_be_taken = BANK
    BANK -= to_be_taken
    print(MSG_I_GAVE_YOU % to_be_taken)


def action_exit():
    raise ExitFlowException


def action_resources():
    show_resources(RESOURCES, BANK)


def action_resolver(action):
    actions = {
        ACTION_BUY: serve_buy,
        ACTION_FILL: serve_fill,
        ACTION_TAKE: serve_take,
        ACTION_REMAINING: action_resources,
        ACTION_EXIT: action_exit,
    }
    return actions[action]


def main():
    while True:
        try:
            action_resolver(ask_question_closed(MSG_WRITE_ACTION % ', '.join(ACTIONS), ACTIONS, str))()
            print()
        except ExitFlowException:
            break
        except GoToMainMenuFlowException:
            continue


if __name__ == '__main__':
    main()
