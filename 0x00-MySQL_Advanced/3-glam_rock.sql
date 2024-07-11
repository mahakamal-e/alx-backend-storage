-- a SQL script that lists all bands with Glam rock
-- as their main style, ranked by their longevity
SELECT band_name,
       CASE
           WHEN formed > 0 AND split > 0 THEN 2022 - formed
           WHEN formed > 0 THEN 2022 - formed
           WHEN split > 0 THEN 2022 - split
           ELSE 0
       END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
