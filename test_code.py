# Adding a test file
def calculate(x, y):
    result = x + y
    return result

def unsafe_query(user_id):
    # This is an intentional security issue for testing
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

