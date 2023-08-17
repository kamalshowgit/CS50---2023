-- write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.
SELECT p.name
FROM people p
JOIN stars s ON p.id = s.person_id
JOIN movies m ON s.movie_id = m.id
WHERE m.year = 2004
ORDER BY p.birth;