from django.contrib.auth import get_user_model
from TestUtils.FattyTestCase import FattyTestBase
from Trainings.models import Training, ExerciseSet, Exercise

User = get_user_model()


class MuscleTypesViewTestCase(FattyTestBase):
    """
    Тесты для muscle-types/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'muscle-types/'

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        perfect_set = {x[0] for x in Exercise.MUSCLE_CHOICES}
        came_set = set(response['muscleTypes'])
        self.assertEqual(perfect_set, came_set, msg='Wrong data came')


class ExercisesViewTestCase(FattyTestBase):
    """
    Тесты для exercises/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'exercises/'
        self.exercise = Exercise.objects.create(name='Hello', muscle_type=Exercise.MUSCLE_CHOICES[0][0])
        self.data_201 = {
            'name': 'test',
            'muscle_type': Exercise.MUSCLE_CHOICES[0][0]
        }
        self.data_400_wrong_choice = {
            'name': 'test',
            'muscle_type': '____',
        }
        self.data_400_not_unique_name = {
            'name': self.exercise.name,
            'muscle_type': self.exercise.muscle_type,
        }

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        self.assertEqual(1, len(response), msg='Wrong response length')
        self.assertEqual(self.exercise.id, response[0]['id'], msg='Wrong id came')

    def testPost201_OK(self):
        response = self.post_response_and_check_status_code(self.url, data=self.data_201)
        new = Exercise.objects.get(id=response['id'])
        self.assertEqual(self.data_201['name'], new.name, msg='Wrong name added')

    def testPost400_WrongChoice(self):
        self.post_response_and_check_status_code(self.url, data=self.data_400_wrong_choice, expected_status_code=400)

    def testPost400_NotUniqueName(self):
        self.post_response_and_check_status_code(self.url, data=self.data_400_not_unique_name, expected_status_code=400)


class CreateExerciseSetView(FattyTestBase):
    """
    Тесты для exercise-sets/
    """
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'exercise-sets/'
        self.exercise = Exercise.objects.create(name='Test', muscle_type=Exercise.MUSCLE_CHOICES[0][0])
        self.training = Training.objects.create(user=self.user)
        self.data_201 = {
            'reps': 10,
            'exercise': self.exercise.id,
            'training': self.training.id,
        }
        self.data_400_wrong_exercise_id = {
            'reps': 10,
            'exercise': self.exercise.id + 1000,
            'training': self.training.id,
        }
        self.data_400_negative_reps = {
            'reps': -10,
            'exercise': self.exercise.id,
            'training': self.training.id,
        }

    def testPost201_OK(self):
        response = self.post_response_and_check_status_code(self.url, data=self.data_201)
        ex_set = ExerciseSet.objects.get(pk=response['id'])
        self.assertEqual(self.data_201['reps'], ex_set.reps, msg='Wrong reps')
        self.assertEqual(1, ex_set.index_number, msg='Wrong index_number')
        self.assertEqual(self.exercise.id, ex_set.exercise.id, msg='Wrong exercise id')

    def testPost400_WrongExerciseId(self):
        self.post_response_and_check_status_code(self.url, data=self.data_400_wrong_exercise_id, expected_status_code=400)

    def testPost400_NegativeReps(self):
        self.post_response_and_check_status_code(self.url, data=self.data_400_negative_reps, expected_status_code=400)


class ExerciseSetViewTestCase(FattyTestBase):
    """
    Тесты для exercise-sets/<pk>/
    """
    def setUp(self):
        super().setUp()
        self.exercise = Exercise.objects.create(name='Test', muscle_type=Exercise.MUSCLE_CHOICES[0][0])
        self.training = Training.objects.create(user=self.user)
        self.exercise_set = ExerciseSet.objects.create(exercise=self.exercise, reps=10, index_number=1, training=self.training)
        self.url = self.url_prefix + f'exercise-sets/{self.exercise_set.id}/'
        self.data_202 = {
            'reps': 20,
            'exercise': self.exercise.id,
        }

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        self.assertEqual(self.exercise_set.id, response['id'], msg='Wrong set returned')

    def testPatch202_OK(self):
        response = self.patch_response_and_check_status_code(self.url, data=self.data_202, expected_status_code=200)
        self.assertEqual(self.data_202['reps'], response['reps'], msg='Wrong reps in response')
        self.exercise_set.refresh_from_db()
        self.assertEqual(self.data_202['reps'], self.exercise_set.reps, msg='Wrong reps in instance')


class TrainingListViewTestCase(FattyTestBase):
    """
    Тесты для trainings/
    """
    def setUp(self):
        super().setUp()
        self.training = Training.objects.create(user=self.user)
        self.url = self.url_prefix + 'trainings/'
        self.data_201 = dict()

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        self.assertEqual(1, len(response['results']), msg='Wrong response length')
        self.assertEqual(self.training.id, response['results'][0]['id'], msg='Wrong id returned')

    def testPost201_OK(self):
        response = self.post_response_and_check_status_code(self.url, data=self.data_201)
        new = Training.objects.get(id=response['id'])
        self.assertEqual(self.user, new.user, msg='Wrong user added')


class TrainingViewTestCase(FattyTestBase):
    """
    Тесты для trainings/<pk>/
    """
    def setUp(self):
        super().setUp()
        self.training = Training.objects.create(user=self.user)
        self.url = self.url_prefix + f'trainings/{self.training.id}/'

    def testGet200_OK(self):
        response = self.get_response_and_check_status_code(self.url)
        self.assertEqual(self.training.id, response['id'], msg='Wrong id returned')

    def testDelete204_OK(self):
        response = self.delete_response_and_check_status_code(self.url)
        self.assertRaises(Training.DoesNotExist, Training.objects.get, id=self.training.id)
