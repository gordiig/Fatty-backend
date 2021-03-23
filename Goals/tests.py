from django.contrib.auth import get_user_model
from TestUtils.FattyTestCase import FattyTestBase

User = get_user_model()


class DailyEatingGoalsViewTestCase(FattyTestBase):
    """
    Тесты для daily-eating-goals/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'daily-eating-goals/'
        self.data_202 = {
            'kcal': 300,
            'carbs': 300,
            'proteins': 300,
            'fats': 300,
        }
        self.data_400_negative = {
            'kcal': -30,
            'carbs': -30,
            'proteins': -30,
            'fats': -30,
        }

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        self.assertEqual(self.user.daly_eating_goals.kcal, response['kcal'], msg='Wrong goals returned')

    def testPatch202_OK(self):
        response = self.patch_response_and_check_status_code(self.url, data=self.data_202, expected_status_code=200)
        self.assertEqual(self.data_202['kcal'], response['kcal'], msg='Wrong in response')
        self.user.refresh_from_db()
        self.assertEqual(self.data_202['kcal'], self.user.daly_eating_goals.kcal, msg='Wrong in instance')

    def testPatch400_NegativeNumbers(self):
        self.patch_response_and_check_status_code(self.url, data=self.data_400_negative, expected_status_code=400)
