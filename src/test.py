from db_interact import init_in_memory_db, read_choices_for_selection_type_from_db
from interfaces import SelectionType


connection = init_in_memory_db()

results = read_choices_for_selection_type_from_db(connection, SelectionType.PROJECTS, "phd")
print(results)