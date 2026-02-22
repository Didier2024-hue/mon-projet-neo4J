import argparse
from neo4j import GraphDatabase

# Configuration de la connexion à Neo4j
def get_driver(user, password):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def calculate_itinerary(driver, start_coords, end_coords):
    query = """
    MERGE (start:TempPoint {x: $start_x, y: $start_y, nom_clean: "Point de départ"})
    MERGE (end:TempPoint {x: $end_x, y: $end_y, nom_clean: "Point d'arrivée"})
    WITH start, end

    MATCH (s_depart:Station)
    WITH start, end, s_depart,
         sqrt((start.x - s_depart.x)^2 + (start.y - s_depart.y)^2) AS dist_depart
    ORDER BY dist_depart ASC LIMIT 1
    MERGE (start)-[:PIETON {distance: dist_depart, temps: dist_depart / 80.0 * 60, type: 'pieton'}]->(s_depart)
    WITH start, end, s_depart

    MATCH (s_arrivee:Station)
    WITH start, end, s_depart, s_arrivee,
         sqrt((end.x - s_arrivee.x)^2 + (end.y - s_arrivee.y)^2) AS dist_arrivee
    ORDER BY dist_arrivee ASC LIMIT 1
    MERGE (s_arrivee)-[:PIETON {distance: dist_arrivee, temps: dist_arrivee / 80.0 * 60, type: 'pieton'}]->(end)
    WITH start, end

    MATCH path = shortestPath((start)-[:PIETON|METRO|CORRESPONDANCE*]-(end))
    WITH path

    WITH path,
         [n IN nodes(path) | n.nom_clean] AS nodes,
         [r IN relationships(path) | r.temps] AS segments,
         reduce(total = 0, r IN relationships(path) | total + r.temps) AS total_time

    MATCH (t:TempPoint) DETACH DELETE t

    RETURN nodes, segments, total_time
    ORDER BY total_time ASC LIMIT 1
    """

    try:
        with driver.session() as session:
            result = session.run(query, {
                'start_x': start_coords[0],
                'start_y': start_coords[1],
                'end_x': end_coords[0],
                'end_y': end_coords[1]
            })
            record = result.single()
            if record is None:
                print("Aucun itinéraire trouvé.")
                return None

            return {
                "nodes": record["nodes"],
                "segments": record["segments"],
                "total_time": record["total_time"]
            }

    except Exception as e:
        print(f" Erreur lors du calcul de l’itinéraire : {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Calculer l\'itinéraire le plus court entre deux points.')
    parser.add_argument('start_coords', type=str, help='Coordonnées de départ (x,y)')
    parser.add_argument('end_coords', type=str, help='Coordonnées d\'arrivée (x,y)')
    parser.add_argument('--neo4j-user', type=str, required=True, help='Nom d\'utilisateur pour Neo4j')
    parser.add_argument('--neo4j-password', type=str, required=True, help='Mot de passe pour Neo4j')

    args = parser.parse_args()

    # Analyser les coordonnées
    start_coords = tuple(map(float, args.start_coords.split(',')))
    end_coords = tuple(map(float, args.end_coords.split(',')))

    # Connexion à Neo4j
    driver = get_driver(args.neo4j_user, args.neo4j_password)

    result = calculate_itinerary(driver, start_coords, end_coords)
    if result:
        print("\n" + "*"*50)
        print("Itinéraire trouvé :")
        print("*"*50)
        print("_"*50)
        print("\n Étapes :", result['nodes'])
        print("_"*50)
        print("\n Segments :", result['segments'])
        print("_"*50)
        print("\n Temps total estimé :", round(result['total_time'], 2), "minutes")
        print("_"*50)
		
    else:
        print(" Aucun itinéraire disponible.")

if __name__ == "__main__":
    main()
