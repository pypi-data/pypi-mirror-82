from collections import OrderedDict
from unittest.mock import patch

from nose.tools import assert_true, eq_

from litmos import User


class TestUser:
    @patch('litmos.litmos.API')
    def test_deactivate(self, api_mock):
        api_mock.update.return_value = True

        user = User({'Id': 'wsGth', 'Active': True})

        assert_true(user.deactivate())

        api_mock.update.assert_called_once_with(
            'users',
            'wsGth',
            OrderedDict([('Id', 'wsGth'),
                         ('UserName', ''),
                         ('FirstName', ''),
                         ('LastName', ''),
                         ('FullName', ''),
                         ('Email', ''),
                         ('AccessLevel', 'Learner'),
                         ('DisableMessages', False),
                         ('Active', False),
                         ('Skype', ''),
                         ('PhoneWork', ''),
                         ('PhoneMobile', ''),
                         ('LastLogin', ''),
                         ('LoginKey', ''),
                         ('IsCustomUsername', False),
                         ('Password', ''),
                         ('SkipFirstLogin', True),
                         ('TimeZone', 'UTC'),
                         ('Street1', ''),
                         ('Street2', ''),
                         ('City', ''),
                         ('State', ''),
                         ('PostalCode', ''),
                         ('Country', ''),
                         ('CompanyName', ''),
                         ('JobTitle', ''),
                         ('CustomField1', ''),
                         ('CustomField2', ''),
                         ('CustomField4', ''),
                         ('CustomField5', ''),
                         ('CustomField6', ''),
                         ('CustomField7', ''),
                         ('CustomField8', ''),
                         ('CustomField9', ''),
                         ('CustomField10', ''),
                         ('Culture', ''),
                         ('ManagerId', ''),
                         ]
                        )
        )

    @patch('litmos.user.API')
    def test_remove_teams(self, api_mock):
        api_mock.remove_sub_resource.return_value = True

        user = User({'Id': 'fgUr2', 'Name': 'User1'})

        assert_true(user.remove_teams())

        api_mock.remove_sub_resource.assert_called_once_with('users',
                                                             user.Id,
                                                             'teams',
                                                             None)

    @patch('litmos.user.API')
    def test_teams(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'SubTeam1'},
            {'Id': 'fgUr2', 'Name': 'SubTeam2'}
        ]

        user = User({'Id': 'fgUr1', 'Name': 'User1'})

        teams = user.teams()

        eq_(len(teams), 2)
        eq_('fgUr3', teams[0].Id)

        api_mock.get_sub_resource.assert_called_once_with('users', 'fgUr1', 'teams')


    @patch('litmos.user.API')
    def test_courses(self, api_mock):
        api_mock.get_sub_resource.return_value = [
            {'Id': 'fgUr3', 'Name': 'Course1'},
            {'Id': 'fgUr2', 'Name': 'Course2'}
        ]

        user = User({'Id': 'fgUr1', 'Name': 'User1'})

        courses = user.courses()

        eq_(len(courses), 2)
        eq_('fgUr3', courses[0].Id)

        api_mock.get_sub_resource.assert_called_once_with('users', 'fgUr1', 'courses')


    @patch('litmos.litmos.API')
    def test_all_full_details(self, api_mock):
        api_mock.all.return_value = [
            {"Id": 'ws5tghd', "Name": "Paul"},
            {"Id": 'ws5tghe', "Name": "James"},
        ]

        api_mock.find.side_effect = [
            {"Id": 'ws5tghd', "Name": "Paul", "CustomField1": "148"},
            {"Id": 'ws5tghe', "Name": "James", "CustomField1": "145"},
        ]

        result = User.all(True)

        eq_(len(result), 2)
        eq_(result[0].Id, 'ws5tghd')
        eq_(result[1].Id, 'ws5tghe')
        eq_(result[0].CustomField1, '148')
        eq_(result[1].CustomField1, '145')

        assert_true(api_mock.all.called)
        eq_(api_mock.find.call_count, 2)

    @patch('litmos.user.API')
    def test_update_advanced_custom_fields(self, api_mock):
        api_mock.add_sub_resource.return_value = True

        user = User({'Id': 'wsGth', 'Active': True})

        fields = [{"Test1": "x"}]
        assert_true(
            user.update_advanced_custom_fields(fields)
        )

        api_mock.add_sub_resource.assert_called_once_with(
            'users',
            user.Id,
            'usercustomfields',
            fields
        )
