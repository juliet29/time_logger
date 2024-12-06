CREATE TABLE focus_area (
    focus_area_name TEXT PRIMARY KEY
);
CREATE TABLE projects (
    project_name TEXT,
    project_focus_area TEXT,
    PRIMARY KEY(project_name, project_focus_area)
    FOREIGN KEY(project_focus_area) REFERENCES focus_area(focus_area_name) ON UPDATE CASCADE
);
CREATE TABLE entry (
    entry_id INTEGER PRIMARY KEY,
    entry_date TEXT,
    entry_project_name TEXT,
    description TEXT,
    FOREIGN KEY(entry_project_name) REFERENCES projects(project_name) ON UPDATE CASCADE
);
CREATE TABLE activity_type(
    activity_type_name TEXT PRIMARY KEY
);

CREATE TABLE entered_activity (
    ea_entry_id INTEGER,
    ea_activity_type_name TEXT,
    PRIMARY KEY(ea_entry_id, ea_activity_type_name)
    FOREIGN KEY(ea_entry_id) REFERENCES entry(entry_id) ON UPDATE CASCADE,
    FOREIGN KEY(ea_activity_type_name) REFERENCES activity_type(activity_type_id) ON UPDATE CASCADE
);

CREATE TABLE time_elapsed(
    time_entry_id INTEGER, 
    minutes_elapsed INTEGER,
    PRIMARY KEY(time_entry_id, minutes_elapsed)
    FOREIGN KEY(time_entry_id) REFERENCES entry(entry_id) ON UPDATE CASCADE
);
