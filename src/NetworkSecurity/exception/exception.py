import sys
from src.NetworkSecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return f"Error occured in python script [{self.file_name}] line number [{self.lineno}] error message [{str(self.error_message)}]"
    