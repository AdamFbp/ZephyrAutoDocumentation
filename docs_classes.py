import json
import os

DEFAULT_FOLDER = '/tests/'

class TestStep:
	def __init__(self, step=None, data=None, expected=None, status=None):
		self.step = step
		self.data = data
		self.expected = expected
		self.status = status

	def set_test_step(self, step):
		self.step = step

	def set_test_data(self, data):
		self.data = data

	def set_expected_result(self, expected):
		self.expected = expected

	def set_status(self, status):
		self.status = status

	def get_dict(self):
		return {'testStep': self.step, 'testData': self.data, 'expectedResult': self.expected, 'status': self.status}

class TestCase:
	def __init__(self, name=None, objective=None, precondition=None, folder=DEFAULT_FOLDER, priority=None):
		self.name = name
		self.objective = objective
		self.precondition = precondition
		self.folder = folder
		self.priority = priority
		self.test_steps = []

	def add_test_step(self, test_step: TestStep):
		self.test_steps.append(test_step)

	def set_name(self, name):
		self.name = name

	def set_objective(self, objective):
		self.objective = objective

	def set_precondition(self, precondition):
		self.precondition = precondition

	def set_folder(self, folder):
		self.folder = folder

	def set_priority(self, priority):
		self.priority = priority

	def get_dict(self):
		return {'name': self.name, 'objective': self.objective, 'precondition': self.precondition, 'folder': self.folder,
				'priority': self.priority, 'testSteps': [step.get_dict() for step in self.test_steps]}


class TestCycle:
	def __init__(self, name=None, description=None, folder=DEFAULT_FOLDER):
		self.name = name
		self.description = description
		self.folder = folder
		self.test_cases = []

	def add_test_case(self, test_case: TestCase):
		self.test_cases.append(test_case)

	def set_name(self, name):
		self.name = name

	def set_description(self, description):
		self.description = description

	def set_folder(self, folder):
		self.folder = folder

	def get_dict(self):
		return {'name': self.name, 'description': self.description, 'folder': self.folder,
				'testCases': [case.get_dict() for case in self.test_cases]}

	def save_to_json(self):
		filename = self.name.replace(' ', '_') + '.json'
		folder_path = os.path.join(os.getcwd(), 'docs')
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		file_path = os.path.join(folder_path, filename)
		json_object = json.dumps(self.get_dict(), indent=4)
		with open(file_path, "w") as outfile:
			outfile.write(json_object)


def try_documentation():
	tcycle1 = TestCycle(name='Proba Ciklus', description='vmi')
	tcase1 = TestCase(name='Proba Case', objective='ez a cel', precondition='tudni, mi az az elofeltetel', priority='magas am')
	tstep11 = TestStep(step='Lepes', data='sok tesztadat', expected='nothing, really', status='passed')
	tstep12 = TestStep(step='Lepes 2', data='sok sok tesztadat', expected='not much', status='passed')
	tcase2 = TestCase(name='Proba Case 2', objective='ez is a cel', precondition='tudni, mi az az elofeltetel', priority='nem is olyan magas')
	tstep21 = TestStep(step='Lepes 21', data='sok tesztadat', expected='nothing, really', status='passed')
	tstep22 = TestStep(step='Lepes 22', data='sok sok tesztadat', expected='not much', status='passed')

	tcase1.add_test_step(tstep11)
	tcase1.add_test_step(tstep12)
	tcycle1.add_test_case(tcase1)
	tcase2.add_test_step(tstep21)
	tcase2.add_test_step(tstep22)
	tcycle1.add_test_case(tcase2)

	tcycle1.save_to_json()

if __name__ == '__main__':
	try_documentation()