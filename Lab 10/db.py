import psycopg2

def connect():
    return psycopg2.connect(
        dbname="snake_game",
        user="postgres",
        password="kaztayd2006",
        host="localhost"
    )

def create_tables():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_score (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    level INTEGER DEFAULT 1,
                    score INTEGER DEFAULT 0
                );
            """)
    print("✅ Tables created.")

def get_or_create_user(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                return user[0]
            else:
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
                return cur.fetchone()[0]

def get_user_progress(user_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT level, score FROM user_score WHERE user_id = %s", (user_id,))
            data = cur.fetchone()
            if data:
                return data
            else:
                cur.execute("INSERT INTO user_score (user_id) VALUES (%s)", (user_id,))
                return (1, 0)

def save_progress(user_id, level, score):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE user_score SET level = %s, score = %s WHERE user_id = %s
            """, (level, score, user_id))
            
def get_top_scores(limit=5):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT u.username, s.score
                FROM user_score s
                JOIN users u ON u.id = s.user_id
                ORDER BY s.score DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()