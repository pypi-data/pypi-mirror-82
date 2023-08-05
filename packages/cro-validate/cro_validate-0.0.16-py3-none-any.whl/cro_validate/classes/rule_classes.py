import inspect

import cro_validate.input.normalize_input as Normalize
from cro_validate.classes.configuration_classes import Config
import cro_validate.classes.definition_classes as Definitions
from cro_validate.classes.util_classes import Boundaries


class Rule:
	def __init__(
				self,
				description,
				callback=None,
				config={},
				boundaries=[]
			):
		self._description = description
		self._callback = callback
		self._config = config
		self._boundaries = boundaries

	def to_json_dict(self):
		return self.get_config()

	def get_config(self):
		return self._config

	def get_boundaries(self):
		return self._boundaries

	def get_description(self):
		return self._description

	def execute(self, fqn, value):
		if self._callback is None:
			return None
		return self._callback(fqn, value, **self.get_config())


########################################################################################################################
#                                                         Noop                                                         #
########################################################################################################################

class Noop(Rule):
	def _noop(self, input_name, value):
		return value

	def __init__(self, description=''):
		super().__init__(
				description=description,
				callback=self._noop
			)


########################################################################################################################
#                                                    DefinitionExists                                                  #
########################################################################################################################

class DefinitionExists(Rule):
	def _def_exists(self, input_name, value):
		if Definitions.Index.exists(value):
			return value
		raise Config.exception_factory.create_input_error(input_name, 'Definition does not exist: {0}.'.format(value))

	def __init__(self):
		super().__init__(
				description='Definition must exist.',
				callback=self._def_exists
			)


########################################################################################################################
#                                                       Numbers                                                        #
########################################################################################################################
class AsInt(Rule):
	def __init__(self):
		super().__init__(
				description='Must be an integer.',
				callback=Normalize.as_int
			)

	def get_boundaries(self):
		return ['InvalidInt']


class IntGte(Rule):
	def __init__(self, minimum):
		super().__init__(
				description='Must be integer greater than or equal to {0}.'.format(minimum),
				callback=Normalize.as_int_greater_than_or_equal_to,
				config={'minimum':minimum}
			)

	def get_boundaries(self):
		return [self.get_config()['minimum'] - 1]


class IntLte(Rule):
	def __init__(self, maximum):
		super().__init__(
				description='Must be integer less than or equal to {0}.'.format(maximum),
				callback=Normalize.as_int_less_than_or_equal_to,
				config={'maximum':maximum}
			)

	def get_boundaries(self):
		bound = self.get_config()['maximum'] + 1
		return [bound]


class FloatGte(Rule):
	def __init__(self, minimum):
		super().__init__(
				description='Must be float greater than or equal to {0}.'.format(minimum),
				callback=Normalize.as_float_greater_than_or_equal_to,
				config={'minimum':minimum}
			)

	def get_boundaries(self):
		return [self.get_config()['minimum'] - 0.1]



class FloatLte(Rule):
	def __init__(self, maximum):
		super().__init__(
				description='Must be float less than or equal to {0}.'.format(maximum),
				callback=Normalize.as_float_less_than_or_equal_to,
				config={'maximum':maximum}
			)

	def get_boundaries(self):
		bound = self.get_config()['maximum'] + 0.1
		return [bound]


class FloatLt(Rule):
	def __init__(self, maximum):
		super().__init__(
				description='Must be float less than {0}.'.format(maximum),
				callback=Normalize.as_float_less_than,
				config={'maximum':maximum}
			)

	def get_boundaries(self):
		return [self.get_config()['maximum']]


########################################################################################################################
#                                                       Strings                                                        #
########################################################################################################################
class MatchRegex(Rule):
	def __init__(self, rex, flags=0, boundaries=[]): # re.IGNORECASE
		super().__init__(				
				description='Must match expression {0}'.format(rex),
				callback=Normalize.as_str_matching_regex,
				config={'rex':rex, 'flags':flags},
				boundaries=boundaries
			)

	def get_boundaries(self):
		return self._boundaries


class StrWithMinLen(Rule):
	def __init__(self, min_len):
		super().__init__(
				description='Must be at least {0} characters long.'.format(min_len),
				callback=Normalize.as_str_with_min_len,
				config={'min_len':min_len}
			)

	def get_boundaries(self):
		min_len = self.get_config()['min_len']
		return Boundaries.get_str_min_len_boundary(min_len)


class StrWithMaxLen(Rule):
	def __init__(self, max_len):
		super().__init__(
				description='Must be no longer than {0} characters.'.format(max_len),
				callback=Normalize.as_str_with_max_len,
				config={'max_len':max_len}
			)

	def get_boundaries(self):
		max_len = self.get_config()['max_len']
		return Boundaries.get_str_max_len_boundary(max_len)


class StrWithinInclusiveLenRange(Rule):
	def __init__(self, min_len, max_len):
		super().__init__(
				description='Must be at least {0} and no more than {1} characters.'.format(min_len, max_len),
				callback=Normalize.as_str_within_inclusive_len_range,
				config={'max_len':max_len, 'min_len':min_len}
			)

	def get_boundaries(self):
		min_len = self.get_config()['min_len']
		max_len = self.get_config()['max_len']
		result = []
		result.extend(Boundaries.get_str_min_len_boundary(min_len))
		result.extend(Boundaries.get_str_max_len_boundary(max_len))
		return result


class ValueInSet(Rule):
	def __init__(self, values):
		desc = 'Must be one of: '
		if len(values) == 1:
			desc = 'Must be: '
		desc = desc + ', '.join(["'{0}'".format(str(entry)) for entry in values])
		if isinstance(values, dict):
			desc = desc + ' (where {0})'.format(', '.join(["'{0}'='{1}'".format(str(entry), values[entry]) for entry in values]))
		desc = desc + '.'
		super().__init__(
				description=desc,
				callback=Normalize.as_value_in_set,
				config={'values':values}
			)

	def get_config(self):
		config = {}
		config.update(self._config)
		values = config['values']
		if isinstance(values, set):
			config['values'] = list(config['values'])
		return config

	def get_boundaries(self):
		s = '___not_in_set___'
		values = self.get_config()['values']
		if s in values:
			raise Config.exception_factory.create_internal_error(
					input_name,
					'Invalid boundary configured: {0} in {1}.'.format(s, values))
		return [s]


	def list_values(self):
		result = list(self.get_config()['values'])
		result.sort()
		return result