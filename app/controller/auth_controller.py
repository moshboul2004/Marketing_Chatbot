import logging
from app.model.auth_model import sign_up, log_in

def handle_sign_up(username, password):
    logging.info("Handling user signup.")

    success = sign_up(username, password)
    
    if success:
        logging.info(f"User {username} signed up successfully.")
        return True
    else:
        logging.warning(f"Signup failed for user {username}. Username might already exist.")
        return False



def handle_log_in(username, password):
    logging.info("Handling user login.")

    success = log_in(username, password)
    
    if success:
        logging.info(f"User {username} logged in successfully.")
        return True
    else:
        logging.warning(f"Login failed for user {username}. Incorrect credentials.")
        return False