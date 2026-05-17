from app.orchestration.configuration_service import (
    ConfigurationService
)

context = (
    ConfigurationService.load_context()
)

print(context.model_dump())