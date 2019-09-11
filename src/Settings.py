import configparser
import logging
import os

logger = logging.getLogger("Settings")

class ConfigSettings:
    """
    Wraps access to a configuration file, allowing the storage to be swapped out as needed
    """

    serviceEndpoint = None
    predictionKey = None
    predictionResourceId = None
    publishIterationName = None
    projectId = None
    boundingBoxScoreThreshold = 0.0
    tempFilePath = None

    def __init__(self, file = None):
        
        if file is None:
            logger.info("No conig file specified - creating default config.")
        else:
            if os.path.exists(file) is False:
                raise FileNotFoundError()

            # Read config section
            logger.info(f"Reading configuration settings from file {file}...")
            config = configparser.ConfigParser();
            config.read(file)
            
            if "CustomVisionService" not in config:
                raise Exception("Required configuration file section ('CustomVisionService') not found!")
        
            if "UtilityDefaults" not in config:
                raise Exception("Required configuration file section ('UtilityDefaults') not found!")

            customVisionSection = config["CustomVisionService"]
            self.serviceEndpoint = customVisionSection["ServiceEndpoint"]
            self.predictionKey = customVisionSection["PredictionKey"]
            self.predictionResourceId = customVisionSection["PredictionResourceId"]
            self.publishIterationName = customVisionSection["PublishIterationName"]
            self.projectId = customVisionSection["ProjectId"]

            utilitySection = config["UtilityDefaults"]
            self.boundingBoxScoreThreshold = float(utilitySection["BoundingBoxScoreThreshold"])
            self.tempFilePath = utilitySection["TempFilePath"]
    
    def DumpSettingsToLog(self):
        logger.info("Configured with the following settings:")
        logger.info(f"BoudingBoxScoreThreshold = {self.boundingBoxScoreThreshold}")
        logger.info(f"TempFilePath = {self.tempFilePath}")
        
        # NOTE we are redacting the Custom Vision service settings as to not end up with secrets 
        # in log streams.