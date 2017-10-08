# CalHack4.0

This is a team project for CalHack4.0 at Berkeley.

What it does:
Recommends potential course schedules for students according to their preference of professor grading, course difficulty and travel distance.
We came up with this idea because currently students have to jump among different platforms to get access to professor quality, course difficulty, travel routes and other information to determine their schedule, which is extremely time consuming and tiring.

What we have done:
1) Collected selected data in the following three areas and form a central database
    a) Write Java program from scratch to collect data from www.berkeleytime.com, a website storing past course information such as section location & time, instructor, average GPA and grade distribution
    b) With help of python urllib and beauitifulSoup, get access to data on www.ratemyprofessors.com, a website that has students' reviews for professors
    c) Collected walking and cycling distances between main buildings on the campus
2) Normalized three indices - course difficulty, professor grading and travel distance
3) Utilized above three indices to recommend students with possible course schedules that are conflict-free and tailored to student’s preference

What could be improved:
1) Get future semester data to enable its prediction function
2) incorporated more indices to improve grading algorithm towards higher diversity and accuracy
3) Implemented Google API to dynamically display and recommend route for schedule
