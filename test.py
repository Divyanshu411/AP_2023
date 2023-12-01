import unittest
import os
from unittest.mock import patch, call
from io import StringIO
from ap2 import read_integer_between_numbers, race_results, users_venue, competitors_by_county, displaying_winners_of_each_race, relevant_runner_info, displaying_runners_who_have_won_at_least_one_race, main


class TestDone(unittest.TestCase):

    @patch('builtins.input', side_effect=['5'])
    def test_read_integer_between_numbers_valid_input(self, mock_input):
        result = read_integer_between_numbers("Enter a number between 1 and 7: ", 1, 7, input_function=mock_input)
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=['1'])
    def test_race_results_valid_input(self, mock_input):
        races_location = ['Kinsale', 'Blarney', 'Newmarket', 'Youghal', 'Castletownbere']
        with patch('sys.stdout', new_callable=StringIO):
            id, time_taken, venue = race_results(races_location, 1)
        self.assertEqual(len(id), len(time_taken))
        self.assertEqual(venue, races_location[0])

    @patch('builtins.input', side_effect=['2', 'Cork', '1.0', '1', '1', '1', '1', '1', '1', '1', '1', '1'])
    def test_users_venue_input_menu_2(self, mock_input):
        races_location = ['Kinsale', 'Blarney', 'Newmarket', 'Youghal', 'Castletownbere']
        runners_id = ['CK-24', 'CK-23', 'KY-43', 'CK-11', 'KY-12', 'TP-02', 'WD-32', 'LK-73', 'WD-19']

        with patch('sys.stdout', new_callable=StringIO):
            users_venue(races_location, [], runners_id)

        new_location_file = 'Cork.txt'
        self.assertTrue(os.path.exists(new_location_file))

        # Assert the results for each runner in the new location file
        with open(new_location_file, 'r') as file:
            lines = file.readlines()
            expected_results = ['CK-24,1\n', 'CK-23,1\n', 'KY-43,1\n', 'CK-11,1\n', 'KY-12,1\n', 'TP-02,1\n',
                                'WD-32,1\n', 'LK-73,1\n', 'WD-19,1\n']
            self.assertEqual(lines, expected_results)

    @patch('builtins.open', new_callable=lambda: lambda _: StringIO(
        'Clare,Cl\nCork,CK\nKerry,KY\nLimerick,LK\nTipperary,TP\nWaterford,WD\n'))
    @patch('sys.stdout', new_callable=StringIO)
    def test_competitors_by_county_input_menu_3(self, mock_stdout, mock_open):
        # Prepare input data for the test
        runners_name = ["Anna Fox", "Des Kelly", "Joe Flynn", "Ann Cahill", "Sally Fox", "Sil Murphy", "Joe Shine",
                        "Lisa Collins", "Des Kelly"]
        runners_id = ["CK-24", "CK-23", "CK-11", "KY-43", "KY-12", "LK-73", "TP-02", "WD-32", "WD-19"]

        competitors_by_county(runners_name, runners_id)

        expected_output = (
            "\nClare runners\n"
            "====================\n"

            "\nCork runners\n"
            "====================\n"
            "Anna Fox (CK-24)\n"
            "Des Kelly (CK-23)\n"
            "Joe Flynn (CK-11)\n"

            "\nKerry runners\n"
            "====================\n"
            "Ann Cahill (KY-43)\n"
            "Sally Fox (KY-12)\n"

            "\nLimerick runners\n"
            "====================\n"
            "Sil Murphy (LK-73)\n"

            "\nTipperary runners\n"
            "====================\n"
            "Joe Shine (TP-02)\n"

            "\nWaterford runners\n"
            "====================\n"
            "Lisa Collins (WD-32)\n"
            "Des Kelly (WD-19)\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


    @patch('ap2.reading_race_results')
    @patch('ap2.winner_of_race')
    def test_displaying_winners_of_each_race_input_menu_4(self, mock_winner_of_race, mock_reading_race_results):
        races_location = ['Kinsale', 'Blarney', 'Newmarket', 'Youghal', 'Castletownbere']
        mock_winner_of_race.side_effect = ['LK-73', ' KY-43', 'WD-32', 'TP-02', 'KY-12']
        mock_reading_race_results.side_effect = [
            (
            ['KY-43', 'CK-11', 'CK-23', 'WD-32', 'TP-02', 'WD-19', 'LK-73'],
            [1915, 1845, 1900, 1808, 1825, 2026, 211]),
            (['KY-43', 'CK-11', 'CK-23', 'WD-32', 'TP-02', 'WD-19', 'LK-73'],
             [1915, 2045, 2020, 1928, 2020, 1926, 2131]),
            (['KY-43', 'CK-11', 'CK-23', 'WD-32', 'TP-02', 'WD-19', 'LK-73'],
             [1915, 2245, 2000, 1728, 1825, 1756, 2111]),
            (['KY-43', 'CK-11', 'CK-23', 'WD-32', 'TP-02', 'WD-19', 'LK-73'],
             [1785, 1845, 1900, 1758, 1725, 1726, 1811]),
            (['CK-24', 'KY-43', 'WD-32', 'TP-02', 'WD-19', 'LK-73', 'CK-23', 'KY-12'],
             [2001, 1951, 302, 1925, 2226, 1991, 2040, 0])]

        with patch('builtins.print') as mock_print:
            displaying_winners_of_each_race(races_location)

        expected_calls = [call('Venue             Winner'),
                          call('========================'),
                          call('Kinsale           LK-73'),
                          call('Blarney            KY-43'),
                          call('Newmarket         WD-32'),
                          call('Youghal           TP-02'),
                          call('Castletownbere    KY-12')]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('ap2.read_integer_between_numbers', return_value=1)
    def test_relevant_runner_info_input_menu_5(self, input):
        runners_name = ["Anna Fox", "Des Kelly", "Ann Cahill"]
        runners_id = ["CK-24", "CK-23", "KY-43"]
        expected_runner = "Anna Fox"
        expected_id = "CK-24"
        runner, id = relevant_runner_info(runners_name, runners_id)
        self.assertEqual(runner, expected_runner)
        self.assertEqual(id, expected_id)

    @patch('builtins.print')
    def test_display_runners_who_won_at_least_once_input_menu_6(self, mock_print):
        races_location = ['Kinsale', 'Blarney', 'Newmarket', 'Youghal', 'Castletownbere']
        runners_name = ["Anna Fox", "Des Kelly", "Joe Flynn", "Ann Cahill", "Sally Fox", "Sil Murphy", "Joe Shine",
                        "Lisa Collins", "Des Kelly"]
        runners_id = ["CK-24", "CK-23", "CK-11", "KY-43", "KY-12", "LK-73", "TP-02", "WD-32", "WD-19"]

        displaying_runners_who_have_won_at_least_one_race(races_location, runners_name, runners_id)

        expected_calls = [
            call('The following runners have all won at least one race:'),
            call('-' * 55),
            call('Sil Murphy (LK-73)'),
            call('Ann Cahill (KY-43)'),
            call('Lisa Collins (WD-32)'),
            call('Joe Shine (TP-02)'),
            call('Sally Fox (KY-12)'),
        ]

        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('builtins.input', side_effect=['7'])
    def test_quit_application_input_menu_7(self, mock_input):
        with patch('sys.stdout') as mock_stdout:
            main()

        mock_stdout.assert_not_called()


if __name__ == '__main__':
    unittest.main()
