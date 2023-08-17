-- write a SQL query to list the names of all people who starred in Toy Story.
SELECT p.name
FROM people p
JOIN stars s ON p.id = s.person_id
JOIN movies m ON s.movie_id = m.id
WHERE m.title = 'Toy Story';
