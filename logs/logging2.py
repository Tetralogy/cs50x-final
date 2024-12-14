import logging
import functools
import os

# Create a global logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Simple feature toggle for logging
class FeatureLogger:
    # Dictionary to track enabled features
    _enabled_features = {}

    @classmethod
    def enable(cls, *features):
        """
        Enable logging for specific features.
        Usage: FeatureLogger.enable('user', 'payment')
        """
        for feature in features:
            cls._enabled_features[feature] = True
            pxrint(f"✅ Logging enabled for: {feature}")

    @classmethod
    def disable(cls, *features):
        """
        Disable logging for specific features.
        Usage: FeatureLogger.disable('user', 'payment')
        """
        for feature in features:
            cls._enabled_features[feature] = False
            pxrint(f"❌ Logging disabled for: {feature}")

    @classmethod
    def log(cls, feature, message, level=logging.INFO):
        """
        Log a message for a specific feature if it's enabled.
        Usage: FeatureLogger.log('user', 'User created', logging.DEBUG)
        """
        if cls._enabled_features.get(feature, False):
            logging.log(level, f"[{feature.upper()}] {message}")

# Decorator for easy function logging
def feature_log(feature):
    """
    Decorator to log function calls for a specific feature.
    Usage:
    @feature_log('user')
    def create_user():
        # function body
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log function entry
            FeatureLogger.log(feature, f"Entering {func.__name__}")
            
            try:
                # Execute the function
                result = func(*args, **kwargs)
                
                # Log function exit
                FeatureLogger.log(feature, f"Exiting {func.__name__}")
                
                return result
            
            except Exception as e:
                # Log any exceptions
                FeatureLogger.log(feature, f"Error in {func.__name__}: {str(e)}", logging.ERROR)
                raise
        return wrapper
    return decorator

# Example usage in a Flask-like application
class UserService:
    @feature_log('user')
    def create_user(self, username):
        # Simulated user creation
        FeatureLogger.log('user', f"Creating user: {username}")
        return f"User {username} created"

    @feature_log('user')
    def delete_user(self, username):
        # Simulated user deletion
        FeatureLogger.log('user', f"Deleting user: {username}")
        return f"User {username} deleted"

# Demonstration of usage
if __name__ == '__main__':
    # Enable logging for specific features
    FeatureLogger.enable('user')
    
    # Create a service instance
    user_service = UserService()
    
    # These calls will be logged
    user_service.create_user('alice')
    user_service.delete_user('bob')
    
    # Disable user feature logging
    FeatureLogger.disable('user')
    
    # This won't be logged
    user_service.create_user('charlie')