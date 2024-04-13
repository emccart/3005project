INSERT INTO Users (email, passw, name, is_trainer) VALUES
('admin', 'passwordhashed', 'admin', FALSE),
('adam.anderson@email.com', 'adamhashed', 'Adam Anderson', FALSE),
('ben.bertrand@email.com', 'benhashed', 'Ben Bertrand', FALSE),
('charles.clark@email.com', 'charleshashed', 'Charles Clark', TRUE),
('dave.daniel@email.com', 'davehashed', 'David Daniel', FALSE);

INSERT INTO Rooms (descript) VALUES
('Treadmills'),
('Pool'),
('Yoga Room'),
('Climbing Wall');

INSERT INTO Classes (teacher_id, room_id, capacity, class_name, start_time, duration, start_date) VALUES
(4, 2, 1, 'Personal Swimming Lesson', '8:00', '2:00', '2024-05-01'),
(4, 3, 3, 'Group Yoga', '10:30', '1:30', '2024-05-08');

INSERT INTO Attendance (class_id, member_id) VALUES
(2, 2);

INSERT INTO Equipment (equip_name, last_maint) VALUES
('Treadmill 1', CURRENT_DATE),
('Treadmill 2', '1991-01-05'),
('Lifeguard Chair', '1700-06-04'),
('Climbing Wall', CURRENT_DATE);

INSERT INTO Goals (member_id, descript) VALUES
(2, 'Climb 5 times'),
(2, 'Learn how to swim'),
(3, 'Lose 5 pounds');

INSERT INTO Payments (user_id, amount_cents) VALUES
(2, 3000),
(3, 3000),
(5, 3000);