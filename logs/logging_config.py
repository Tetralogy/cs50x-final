import logging
import logging.handlers
import sys
import os
from typing import Optional, Union, Dict, Any

LOGGING_LEVEL = logging.DEBUG
class LoggerFactory:
    """
    A professional-grade logging configuration factory that follows Python's 
    recommended logging practices.
    """
    
    @staticmethod
    def create_logger(
        name: str,
        level: int = LOGGING_LEVEL,
        log_file: Optional[str] = None,
        console: bool = True,
        format_string: Optional[str] = None,
        max_file_bytes: int = 1 * 1024 * 1024,  # 1 MB
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Create a fully configured logger with multiple output options.
        
        Args:
            name (str): Name of the logger (typically __name__)
            level (int): Logging level (e.g., logging.INFO, logging.DEBUG)
            log_file (str, optional): Path to log file for file logging
            console (bool): Whether to log to console
            format_string (str, optional): Custom log format
            max_file_bytes (int): Maximum size of log file before rotation
            backup_count (int): Number of backup log files to keep
        
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:

            # Default formatting if not provided
            if not format_string:
                format_string = (
                    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s '
                    '[%(filename)s:%(lineno)d] - %(message)s'
                )
            formatter = logging.Formatter(format_string)

            # Console handler
            if console:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(level)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            # File handler with rotation
            if log_file:
                # Ensure log directory exists
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=max_file_bytes,
                    backupCount=backup_count
                )
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        # Prevent propagation to parent loggers
        logger.propagate = False

        return logger

class ApplicationLogger:
    """
    A class to manage logging configuration across an entire application.
    Follows the principle of centralized logging configuration.
    """
    _loggers: Dict[str, logging.Logger] = {}
    _default_config: Dict[str, Any] = {
        'level': LOGGING_LEVEL,
        'console': True,
        'log_file': None
    }

    @classmethod
    def configure(
        cls, 
        default_level: int = LOGGING_LEVEL, 
        log_file: Optional[str] = 'app.log'
    ):
        """
        Configure global logging settings for the entire application.
        
        Args:
            default_level (int): Default logging level
            log_file (str, optional): Default log file path
        """
        cls._default_config.update({
            'level': default_level,
            'log_file': log_file
        })

    @classmethod
    def get_logger(
        cls, 
        name: Optional[str] = None, 
        level: Optional[int] = None
    ) -> logging.Logger:
        """
        Get or create a logger with optional custom configuration.
        
        Args:
            name (str, optional): Name of the logger (defaults to root logger)
            level (int, optional): Logging level override
        
        Returns:
            logging.Logger: Configured logger instance
        """
        # Use module name if not provided
        logger_name = name or '__root__'
        
        # Check if logger already exists
        if logger_name in cls._loggers:
            return cls._loggers[logger_name]
        
        # Create new logger
        config = cls._default_config.copy()
        if level is not None:
            config['level'] = level
        
        logger = LoggerFactory.create_logger(
            name=logger_name,
            level=config['level'],
            log_file=config['log_file'],
            console=config['console']
        )
        
        # Cache the logger
        cls._loggers[logger_name] = logger
        
        return logger

def configure_logging(app):
    # Configure application-wide logging
    ApplicationLogger.configure(
        default_level=LOGGING_LEVEL,
        log_file='logs/application.log'
    )
    logger = ApplicationLogger.get_logger(__name__)
    logger.debug("Application logging configured")
        # Get the logger for list_utils.py
    #isolated_module_logger = ApplicationLogger.get_logger('application.list_utils')
    #isolated_module_logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG for list_utils.py

    try:
        # Log application startup
        logger.info(f"Application started in {os.environ.get('FLASK_ENV')} environment")

        # CRITICAL PART: Override Flask's logger to use our global logging system
        # This ensures all Flask logs go through our single logging configuration
        app.logger.handlers = []  # Remove default Flask handlers
        app.logger.propagate = True  # Ensure logs are passed to root logger

        # Optional: You can still set Flask-specific logging behavior if needed
        #app.logger.setLevel(logging_level)

    except Exception as e:
        # Fallback error reporting
        print(f"Logging configuration failed: {e}")
        

def perform_critical_operation():
    """
    Example function demonstrating logging
    """
    logger = ApplicationLogger.get_logger(__name__)
    logger.info("Performing critical operation")
    # Some business logic here
    return "Success"

""" if __name__ == '__main__':
    main() """