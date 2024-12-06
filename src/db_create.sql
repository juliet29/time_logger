CREATE TABLE focus_area (
    focus_area_name TEXT PRIMARY KEY
);
CREATE TABLE projects (
    project_name TEXT PRIMARY KEY
);
CREATE TABLE entry (
    entry_id INTEGER PRIMARY KEY,
    entry_date TEXT,
    entry_focus_area TEXT,
    FOREIGN KEY(entry_focus_area) REFERENCES focus_area(focus_area_name),
    entry_project_name TEXT,
    FOREIGN KEY(entry_project_name) REFERENCES projects(project_name),
    description TEXT
);
CREATE TABLE entered_activity (
    entered_activity_entry_id INTEGER PRIMARY KEY,
    FOREIGN KEY(entered_activity_entry_id) REFERENCES entry(entry_id),
    entered_activity_activity_type_name TEXT PRIMARY KEY,
    FOREIGN KEY(entered_activity_activity_type_name) REFERENCES activity_type(activity_type_id)
);
CREATE TABLE activity_type(
    activity_type_name TEXT PRIMARY KEY
);

CREATE TABLE time_elapsed(
    time_entry_id INTEGER PRIMARY KEY, 
    FOREIGN KEY(time_entry_id) REFERENCES entry(entry_id);
    minutes_elapsed INTEGER PRIMARY KEY
);
