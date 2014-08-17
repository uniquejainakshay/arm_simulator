error_type =  []
class break_point_exception(Exception):
	def __init__(self, inst_index):
		self.Type = "break_point_exception"
		self.inst_index = inst_index


class text_end_exception(Exception):
	def __init__(self, inst_index):
		self.Type = "text_end_exception"
		self.inst_index = inst_index


class register_watch_exception(Exception):
	def __init__(self, reg_name):
		self.Type = "register_watch_exception"
		self.reg_name  = reg_name

