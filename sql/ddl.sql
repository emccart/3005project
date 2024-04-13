CREATE TABLE IF NOT EXISTS Users (
	user_id SERIAL PRIMARY KEY,
	email VARCHAR(255) UNIQUE NOT NULL,
	passw VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	is_trainer BOOLEAN
);

CREATE TABLE IF NOT EXISTS Rooms (
	room_id SERIAL PRIMARY KEY,
	descript TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Classes (
	class_id SERIAL PRIMARY KEY,
	teacher_id INT REFERENCES Users (user_id),
	room_id INT REFERENCES Rooms (room_id),
	capacity INT NOT NULL DEFAULT 1,
	class_name VARCHAR(255) NOT NULL,
	start_time TIME NOT NULL,
	duration TIME NOT NULL,
	start_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Attendance (
	att_id SERIAL PRIMARY KEY,
	class_id INT REFERENCES Classes (class_id),
	member_id INT REFERENCES Users (user_id)
);

CREATE TABLE IF NOT EXISTS Equipment (
	equip_id SERIAL PRIMARY KEY,
	equip_name VARCHAR(255) NOT NULL,
	last_maint DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS Goals (
	goal_id SERIAL PRIMARY KEY,
	member_id INT REFERENCES Users (user_id),
	descript TEXT NOT NULL,
	completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Payments (
	pay_id SERIAL PRIMARY KEY,
	user_id INT REFERENCES Users (user_id),
	amount_cents INT
);