from pycomm3 import LogixDriver


def write_single():
    with LogixDriver('10.61.50.4/10') as plc:
        return plc.write(('DINT2', 100_000_000))


def write_multiple():
    with LogixDriver('10.61.50.4/10') as plc:
        return plc.write(('REAL2', 25.2), ('STRING3', 'A test for writing to a string.'))


def write_structure():

    with LogixDriver('10.61.50.4/10') as plc:
        recipe_data = [
            True,
            [10, 11, 4, 20, 6, 20, 6, 30, 5, 0],
            [100, 500, 85, 5, 15, 10.5, 20, 0, 0, 0],
            ['Set Water Temperature',
             'Heated Water',
             'Start Agitator',
             'Hand Add - Flavor Part 1',
             'Timed Mix',
             'Hand Add - Flavor Part 2',
             'Timed Mix',
             'Transfer to Storage Tank',
             'Disable Agitator',
             ''],
            ['°F', 'lbs', '%', 'gal', 'min', 'lbs', 'min', '', '', ''],
            'Our Fictional Recipe'
        ]

        plc.write(('Example_Recipe', recipe_data))